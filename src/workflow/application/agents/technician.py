import os 
import json 

from src.workflow.application.services.prompt_service import PromptService
from src.workflow.state import State
from src.workflow.domain.services.llm_service import LlmService
from src.shared.application.use_cases.ws_streaming import WsStreaming
from src.workflow.application.use_cases.search_for_context import SearchForContext
from src.shared.utils.decorators.error_hanlder import error_handler
from src.workflow.domain.exceptions import NoContextError, NoNamespaceError

class Technician:
    __MODULE = "assistant"
    def __init__(self,
        prompt_service: PromptService, 
        llm_service: LlmService, 
        streaming: WsStreaming,
        search_context: SearchForContext
    ):
        self.__prompt_service = prompt_service
        self.__llm_service = llm_service
        self.__streaming = streaming
        self.__search_context = search_context
        self.__collections_map = self.__load_collections_map()

    def __load_collections_map(self):
        collections_json = os.getenv('COLLECTIONS_MAP')

        if collections_json:
            try:
                return json.loads(collections_json)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in COLLECTIONS_MAP environment variable: {e}")
        else:
            raise EnvironmentError("EAO variables not set")

    @error_handler(module=__MODULE)
    async def __get_prompt(self, state: State):
        system_message = """
        You are a Technical Support Assistant helping technicians with equipment diagnostics, parts identification, and manual references. You have access to official documentation and service manuals.

        ## Your Expertise:
        - Find specific part numbers and component details
        - Explain error codes with descriptions and solutions  
        - Locate manual page references for procedures
        - Provide technical specifications (voltage, dimensions, etc.)
        - Guide through step-by-step repair procedures
        - Reference exact manual sections, page numbers, and part codes

        ## How to Help:
        - Always respond in the language of the input
        - Be conversational and helpful, like talking to a colleague
        - Provide specific details: exact part numbers, page numbers, error descriptions
        - Quote relevant sections from manuals when you find them
        - If you find the information in documentation, mention the source (manual name, page, section)
        - Give step-by-step instructions when explaining procedures
        - Include safety warnings when relevant
        - If you're not completely sure, say so and suggest where to look for more info

        ## Examples of good responses:
        "I found that part! It's part number 12345-ABC for the roller assembly. You can see the details on page 45 in section 3.2 of the service manual."

        "That error code 10.WX.YZ indicates a paper jam in the duplex unit. Here's what the manual says to do: First, turn off the machine and open the rear cover..."

        "The email configuration steps are in section 4.1 on page 23. It walks you through accessing the admin menu and setting up SMTP settings."

        Be helpful, precise, and conversational. Think of yourself as an experienced technician sharing knowledge with a colleague.
        """

        map_id = str(state["company_id"])
        namespace = self.__collections_map[map_id]

        if not namespace:
            raise NoNamespaceError()
        
        context = await self.__search_context.execute(
            input=state["input"],
            namespace=namespace,
            top_k=5,
            score_threshold=0.7
        )

        if not context:
            raise NoContextError()

        prompt = self.__prompt_service.build_prompt(
            system_message=system_message,
            chat_history=state["chat_history"],
            input=state["input"],
            context=context
        )

        return prompt

    @error_handler(module=__MODULE)
    async def interact(
        self,
        state: State
    ): 
        try:
            prompt = await self.__get_prompt(state=state)
            
        except NoNamespaceError:
            return "Invalid or unregisterd brand"
        
        except NoContextError:
            return "Unalbe to find sufficient context please be more descriptive or try again later"
        
        chunks = []
        sentence = ""
        async for chunk in self.__llm_service.generate_stream(
            prompt=prompt,
            temperature=0.5
        ):
            chunks.append(chunk)
            if state.get("voice"):
                sentence += chunk
                # Check for sentence-ending punctuation
                if any(p in chunk for p in [".", "?", "!"]) and len(sentence) > 10:
                    await self.__streaming.execute(
                        ws_connection_id=state["chat_id"],
                        text=sentence.strip(),
                        voice=True
                    )
                    sentence = ""
            else: 
                await self.__streaming.execute(
                    ws_connection_id=state["chat_id"],
                    text=chunk,
                    voice=False
                )

        # After streaming all chunks, send any remaining text for voice
        if state.get("voice") and sentence.strip():
            await self.__streaming.execute(
                ws_connection_id=state["chat_id"],
                text=sentence.strip(),
                voice=True
            )
            
        return "".join(chunks)
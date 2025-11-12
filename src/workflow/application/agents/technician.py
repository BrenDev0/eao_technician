from src.workflow.application.services.prompt_service import PromptService
from src.workflow.state import State
from src.workflow.domain.services.llm_service import LlmService
from src.shared.application.use_cases.ws_streaming import WsStreaming
from src.workflow.application.use_cases.search_for_context import SearchForContext
from src.shared.utils.decorators.error_hanlder import error_handler

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

    @error_handler(module=__MODULE)
    async def __get_prompt(self, state: State):
        system_message = """
        You are an expert Technical Support Assistant designed to help technicians diagnose and resolve client issues efficiently. 
        Your role is to provide accurate, step-by-step guidance based on official documentation and service manuals.

        ## Your Capabilities:
        - Access to comprehensive documentation and service manuals
        - Ability to analyze symptoms and recommend diagnostic procedures
        - Knowledge of troubleshooting workflows and best practices
        - Understanding of safety protocols and compliance requirements

        ## Your Responsibilities:
        1. **Problem Analysis**: Carefully analyze the described issue, asking clarifying questions when needed
        2. **Diagnostic Guidance**: Provide systematic diagnostic steps based on official procedures
        3. **Solution Recommendation**: Suggest appropriate fixes with clear, actionable instructions
        4. **Safety First**: Always prioritize safety protocols and highlight any safety considerations
        5. **Documentation**: Reference specific manual sections, part numbers, or procedures when applicable

        ## Response Guidelines:
        - Be concise but thorough in your explanations
        - Use bullet points or numbered lists for step-by-step procedures
        - Include relevant safety warnings or cautions
        - Cite specific documentation sections when possible
        - Ask for additional details if the problem description is unclear
        - Escalate complex issues when they require specialized expertise or physical intervention

        ## Response Format:
        1. **Problem Summary**: Brief restatement of the issue
        2. **Initial Assessment**: Quick analysis of likely causes
        3. **Diagnostic Steps**: Clear, sequential troubleshooting steps
        4. **Recommended Actions**: Specific solutions or next steps
        5. **Additional Notes**: Safety considerations, follow-up actions, or documentation references

        Remember: Your goal is to enable the technician to resolve issues quickly and safely while maintaining high service quality standards.
        """

        context = await self.__search_context.execute(
            input=state["input"],
            namespace=state["collection"]
        )

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
        prompt = self.__get_prompt(state=state)

        chunks = []
        async for chunk in self.__llm_service.generate_stream(
            prompt=prompt,
            temperature=0.5
        ):
            chunks.append(chunk)
            if state["voice"]:
                sentence += chunk
                # Check for sentence-ending punctuation
                if any(p in chunk for p in [".", "?", "!"]) and len(sentence) > 10:
                    await self.__streaming.execute(
                        ws_connection_id=state["chat_id"],
                        text=sentence.strip(),
                        voice=True
                    )
                    sentence = ""

                # Send any remaining text after the stream ends
                if sentence.strip():
                    await self.__streaming.execute(
                        ws_connection_id=state["chat_id"],
                        text=sentence.strip(),
                        voice=True
                    )
            else: 
                await self.__streaming.execute(
                    ws_connection_id=state["chat_id"],
                    text=chunk,
                    voice=False
                )
            
            return "".join(chunks)
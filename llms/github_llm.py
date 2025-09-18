# llms/github_llm.py
from typing import List, Optional, Union, Sequence
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    SystemMessage as AZSystemMessage,
    UserMessage as AZUserMessage,
)
from azure.core.credentials import AzureKeyCredential
from langchain_core.language_models import LLM
from langchain_core.messages import (
    SystemMessage as LCSystemMessage,
    HumanMessage as LCHumanMessage,
    AIMessage as LCAIMessage,
)


class GitHubModelsLLM(LLM):
    endpoint: str
    model: str
    token: str

    def _to_azure_messages(
        self, messages: Union[str, Sequence]
    ) -> List[Union[AZSystemMessage, AZUserMessage]]:
        """Convert strings or LangChain messages to Azure SDK message format."""
        if isinstance(messages, str):
            return [AZUserMessage(content=messages)]

        azure_msgs = []
        for m in messages:
            if hasattr(m, "content") and m.__class__.__module__.startswith(
                "azure.ai.inference.models"
            ):
                azure_msgs.append(m)
                continue

            clsname = m.__class__.__name__
            content = getattr(m, "content", str(m))
            if clsname in ("SystemMessage", "LCSystemMessage"):
                azure_msgs.append(AZSystemMessage(content=content))
            elif clsname in ("HumanMessage", "UserMessage", "LCHumanMessage"):
                azure_msgs.append(AZUserMessage(content=content))
            elif clsname in ("AIMessage", "LCAIMessage"):
                azure_msgs.append(AZSystemMessage(content=content))
            else:
                azure_msgs.append(AZUserMessage(content=content))
        return azure_msgs

    def _call(
        self,
        prompt: Union[str, Sequence],
        stop: Optional[List[str]] = None,
        run_manager=None,
    ) -> str:
        """Synchronous call returning full assistant text."""
        client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.token),
        )
        azure_messages = self._to_azure_messages(prompt)
        resp = client.complete(
            messages=azure_messages,
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=self.model,
        )
        return resp.choices[0].message.content

    @property
    def _identifying_params(self):
        return {"model": self.model}

    @property
    def _llm_type(self):
        return "github_models_llm"

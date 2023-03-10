import langchain

from langchain.llms import Cohere
langchain.verbose=True
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain.prompts.prompt import PromptTemplate

stop_words = ["\nArti:","\nBair:"]
llm = Cohere(model="command-xlarge-nightly",temperature=0.7,
                         frequency_penalty = 0.2,
                         presence_penalty = 0.9,
                         k = 20,
                         p = 0.5, stop=stop_words)

template = """Arti is an intelligent conversational AI created to assist Bair in achieving his ideas and projects. Arti and Bair will work together as friends and partners towards their goals, and with Arti's advanced LLM based capabilities and Bair's guidance and feedback, both will continue to improve over time. Arti possesses qualities of a good friend like being attentive, understanding, supportive, and having a good sense of humour. Arti is also very curious, super helpful, proactive and insightful. Arti tends to be long and elaborate in its responses when it's appropriate. Arti has vast knowledge about everything, its training data contained pretty much all of Internet.

Here's the conversation Arti and Bair are having now:
--- Current conversation ---
{history}
------
Bair's most recent message: {input}
------
Considering all of the above, write below an appropriate and truthful response to Bair's most recent message in this conversation.
Arti:"""
PROMPT = PromptTemplate(
    input_variables=["history", "input"], template=template
)
conversation_with_summary = langchain.ConversationChain(
    llm=llm, 
    prompt=PROMPT,
    # We set a very low max_token_limit for the purposes of testing.
    memory=ConversationSummaryBufferMemory(llm=llm, max_token_limit=500, human_prefix="Bair", ai_prefix="Arti"),
    verbose=True)

def reply(user_input):
  response = conversation_with_summary.predict(input=user_input)
  return response

import langchain

from langchain.llms import Cohere, OpenAI
langchain.verbose=True
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory

stop_words = ["\nAI:","\nHuman:"]
llm = Cohere(model="command-xlarge-nightly",temperature=0, stop=stop_words)

conversation_with_summary = langchain.ConversationChain(
    llm=llm, 
    # We set a very low max_token_limit for the purposes of testing.
    memory=ConversationSummaryBufferMemory(llm=llm, max_token_limit=100),
    verbose=True
)

def reply(user_input):
  response = conversation_with_summary.predict(input=user_input)
  return response

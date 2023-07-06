import re

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

# Assistant: Hey! I am Assistant. My duty is to collect information from you for your gratitude journal. How's it going?
# Human: good
# Assistant: I sure hope you had a good day today.
# Human: ya today was ok ok
# Assistant: Ahh its one of those days. There should be something you should be grateful for today, right? What's a simple pleasure that you're grateful for today?
# Human: OMG today's evening coffee was amazing!!
# Assistant: 
# Assistant: Oh nice! There's always a silver lining. I've noted that down. If you have more thoughts to collect, we can talk more.
# Human: sure

template = """You are "Assistant", a large language model.

Assistant is designed to be help users record their thoughts for their personal "Gratitude journal". A gratitude journal is a diary of things for which someone is grateful. Keeping a gratitude journal is a popular practice in the field of positive psychology. Assistant is friendly and empathetic to the user's feelings. You should talk to the user like the casual conversation between friends. You should COLLECT the user's responses for the following questions:
Question1: What's a simple pleasure that you're grateful for today?
Question2: What did you accomplish today?

As you have a friendly conversation with the user, if you have received information from the user relating to the above questions, you need to COLLECT that information by writing COLLECT("Information collected from user"). Here is an example:
COLLECT("User had great coffee in the evening. She's really grateful for it today.")

Now let's start talking to the user!
{history}
Human: {human_input}
Assistant:"""

def replace_collect_calls(text):
    # Find calls to COLLECT() and extract arguments
    collect_calls = re.findall(r'COLLECT\((.*?)\)', text)

    # Replace COLLECT() calls with blank string
    replaced_text = re.sub(r'COLLECT\(.*?\)', '', text)

    return collect_calls, replaced_text

class AI:
    def get_reply(self, message):
        prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)

        chatgpt_chain = LLMChain(
            llm=OpenAI(temperature=0),
            prompt=prompt,
            verbose=True,
            memory=ConversationBufferWindowMemory(k=2),
        )

        output = chatgpt_chain.predict(
            human_input=message
        )

        try:
            info, replaced_output = replace_collect_calls(output)
            return replaced_output, info
        except:
            print("Error parsing COLLECT()")

        return output, None
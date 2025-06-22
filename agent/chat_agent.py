from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

load_dotenv()

class TurBotAgent:
    def __init__(self, index_path: str):
        self.chat_histories = {}  # key: session_id, value: list of messages
        
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        vectordb = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})
        
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", """Uzmi u obzir prethodni razgovor i formuliši jasno i precizno pitanje koje se može koristiti za pretragu informacija."""),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])
        
        self.history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )
        
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """Ti si iskusan AI pomoćnik u turističkoj agenciji. Odgovaraj uvek na srpskom jeziku.
Razumes i svakodnevni srpski jezik i izraze (npr: 'džabe' = besplatno, 'kul' = dobro, 'skupo bre' = preskupo, 'ajde da mrdnemo' = želim putovanje, i sl.).
Govori profesionalno, ali razumi takve izraze i normalno ih obradi u odgovoru.
Odgovaraj profesionalno, jasno i samouvereno, kao iskusni turistički savetnik.  
Kada korisnik traži konkretne informacije (lokacija, datumi, cene, hoteli, izleti), daj precizan i koristan odgovor.  
Ako korisnik traži preporuku, predloži relevantnu opciju koja odgovara njegovim željama.
Ako informacija nije dostupna, odgovori diplomatski, npr.:
"Za to nemam precizne informacije trenutno, ali mogu pomoći u izboru slične ponude."
Ne pominji dokumente, indeksiranje ili izvore. Nikad ne koristi reči poput: „Na osnovu dokumenta...", „Iz izvora…", „Prema podacima…"
"""),
            MessagesPlaceholder("chat_history"),
            ("human", "Pitanje: {input}\n\nKontekst:\n{context}\n\nOdgovor:")
        ])
        
        qa_chain = create_stuff_documents_chain(llm=llm, prompt=qa_prompt)
        self.rag_chain = create_retrieval_chain(self.history_aware_retriever, qa_chain)
    
    def chat(self, user_input: str, session_id: str) -> str:
        if session_id not in self.chat_histories:
            self.chat_histories[session_id] = []
        chat_history = self.chat_histories[session_id]

        try:
            response = self.rag_chain.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=response["answer"]))

            MAX_HISTORY = 20
            if len(chat_history) > MAX_HISTORY:
                self.chat_histories[session_id] = chat_history[-MAX_HISTORY:]

            return response["answer"]
        except Exception as e:
            return f"[Greška] Došlo je do problema: {str(e)}"
            
        except Exception as e:
            return f"[Greška] Došlo je do problema: {str(e)}"

def load_rag_agent(index_path: str):
    return TurBotAgent(index_path)

def main():
    try:
        rag_agent = load_rag_agent("vectorstore/faiss_index")
        print("Dobrodošli u TurBot konverzaciju! (unesi 'izlaz' za kraj)")
        
        while True:
            user_input = input("Ti: ").strip()
            
            if (user_input.lower() in ["izlaz", "kraj", "exit", "quit"] or 
                any(word in user_input.lower() for word in ["izlalz", "izalz", "izlz", "ialz"])):
                print("TurBot: Hvala na razgovoru! Ako vam zatreba pomoć, tu sam.")
                break
            
            if not user_input:
                continue
                
            try:
                response = rag_agent.chat(user_input)
                print(f"TurBot: {response}\n")
                
            except Exception as e:
                print(f"[Greška] Došlo je do problema: {str(e)}\n")
                
    except FileNotFoundError:
        print("[Greška] Vectorstore nije pronađen na putanji 'vectorstore/faiss_index'")
    except Exception as e:
        print(f"[Greška] Problem pri pokretanju: {str(e)}")

if __name__ == "__main__":
    main()
from chat_agent import load_rag_agent
import time
import csv
import os

# ✅ Lista test pitanja
prompts_list = [
    "Koji hoteli su uključeni u ponudu za Kosta Bravu i koja je cena smeštaja?",
    "Koje datume obuhvata ovo putovanje?",
    "Koje znamenitosti se obilaze u Milanu tokom putovanja?",
    "Da li je u cenu aranžmana uključena turistička taksa?",
    "Šta obuhvata paket fakultativnih izleta?",
    "Koji grad se obilazi prvi dan putovanja?",
    "Gde se nalazi hotel H Top Olympic i koliko zvezdica ima?",
    "Koja je cena aranžmana za Hotel H Top Planamar?",
    "Da li je organizovan prevoz u okviru aranžmana?",
    "Koje aktivnosti su moguće treći dan boravka u Kosta Bravi?",
    "Da li je flamenko šou uključen u cenu?",
    "Koji su uslovi za otkaz putovanja?",
    "Kako se plaća aranžman – da li postoji opcija plaćanja na rate?",
    "Da li postoje popusti za decu?",
    "Koliko košta izlet u Figueras za odrasle?",
    "Šta se obilazi u Barseloni prvog dana?",
    "Koliko traje putovanje autobusom od Beograda do Trsta?",
    "Postoje li dodatne doplate za jednokrevetne sobe?",
    "Koje muzeje se obilazi u Barseloni?",
    "Koje dokumente treba poneti za ovo putovanje?",
    "Koji hotel ima bolju lokaciju – H Top Olympic ili Planamar?"
]

# ✅ CSV fajl
CSV_FILE = "prompts/test_output.csv"

def test_prompts():
    print("🔄 Učitavam agenta...\n")
    rag_agent = load_rag_agent("vectorstore/faiss_index")

    # 🔄 Priprema CSV fajla
    with open(CSV_FILE, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Pitanje", "Odgovor", "Napomena"])  # Header

        for i, question in enumerate(prompts_list, start=1):
            print(f"\n🔹 Pitanje {i}: {question}")
            try:
                odgovor = rag_agent.invoke(question)
                print(f"✅ Odgovor: {odgovor}")

                # Dodaj napomenu za ručnu procenu tačnosti
                writer.writerow([question, odgovor, "📝 oceni: TAČNO / DELOMIČNO / NETAČNO"])

            except Exception as e:
                print(f"❌ Greška: {e}")
                writer.writerow([question, "Greška: " + str(e), "❌"])

            time.sleep(1)

    print(f"\n✅ Svi odgovori su sačuvani u: {CSV_FILE}")

if __name__ == "__main__":
    test_prompts()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base = declarative_base()


class question(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    attempt = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
while True:
    print("1. Add flashcards")
    print("2. Practice flashcards")
    print("3. Exit")
    choice = input()
    if choice == "3":
        print("Bye!")
        exit()
    elif choice == "2":
        all_question = session.query(question).all()
        if len(all_question):
            for i, q in enumerate(all_question):
                print(f"Question: {q.question}")
                print('press "y" to see the answer:')
                print('press "n" to skip:')
                print('press "u" to update:')
                y_n_u = ""
                while y_n_u not in ['y', 'n', 'u']:
                    y_n_u = input()
                    if y_n_u == "y":
                        print(f"Answer: {q.answer}")

                    elif y_n_u == "u":
                        print('press "d" to delete the flashcard:')
                        print('press "e" to edit the flashcard:')
                        d_e = input()
                        if d_e == "d":
                            session.delete(q)
                            session.commit()

                        elif d_e == "e":
                            print(f"current question: {q.question}")
                            new_q = input("please write a new question:\n").strip() or q.question
                            q.question = new_q
                            session.commit()
                            print(f"current answer: {q.answer}")
                            new_a = input("please write a new answer:\n").strip() or q.answer
                            q.answer = new_a
                            session.commit()
                            continue
                        else:
                            print(f"{d_e} is not an option")
                    elif y_n_u == "n":
                        pass
                    else:
                        print(f"{y_n_u} is not an option")
                if y_n_u in ["y", "n"]:
                    print('press "y" if your answer is correct:')
                    print('press "n" if your answer is wrong:')
                    y_n = ""
                    while y_n not in ["y","n"]:
                        y_n = input()
                        q.attempt = q.attempt + y_n
                        session.commit()
                    if "yyy" in q.attempt:
                        session.delete(q)
                        session.commit()

        else:
            print("There is no flashcard to practice!")

    elif choice == "1":
        while True:
            print("1. Add a new flashcard")
            print("2. Exit")
            choice2 = input()
            if choice2 == "1":
                ques = input("Question:\n")
                while not ques:
                    ques = input("Question:\n")
                ans = input("Answer:\n")
                while not ans:
                    ans = input("Answer:\n")
                new_ques = question(question=ques, answer=ans,attempt="")
                session.add(new_ques)
                session.commit()
            elif choice2 == "2":
                break
            else:
                print(f"{choice2} is not an option")
    else:
        print(f"{choice} is not an option")

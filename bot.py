import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from flask import Flask, render_template, request, jsonify

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")


data = {
   "intents": [
        {"tag": "greeting",
         "patterns": ["Hi","Hi there", "How are you", "Is anyone there?","Hey","Hola", "Hello", "Good day"],
         "responses": ["Hello, Shravani's Chatbot this side, I am here to tell you about Shravani, if you want options for questions type options"],
         "context": [""]
        },
        {"tag": "goodbye",
         "patterns": ["Bye","See you later", "Goodbye", "Nice chatting to you, bye", "Till next time"],
         "responses": ["See you!, You can connect me via email- shravanimjagtap13@gmail.com", "Have a nice day, You can connect me via email- shravanimjagtap13@gmail.com", "Bye! Come back again soon.You can connect me via email- shravanimjagtap13@gmail.com"],
         "context": [""]
        },
        {"tag": "thanks",
         "patterns": ["Thanks", "Thank you", "That's helpful", "Awesome, thanks", "Thanks for helping me"],
         "responses": ["Happy to talk to you!, You can connect me via email- shravanimjagtap13@gmail.com", "Any time! You can connect me via email- shravanimjagtap13@gmail.com", "My pleasure You can connect me via email- shravanimjagtap13@gmail.com"],
         "context": [""]
        },
        {"tag": "noanswer",
         "patterns": [],
         "responses": ["Sorry, can't understand you, You can connect me via email- shravanimjagtap13@gmail.com", "Please give me more info or You can ask me via email- shravanimjagtap13@gmail.com", "Not sure I understand"],
         "context": [""]
        },
        {"tag": "options",
         "patterns": ["Options","options","sample questions","How you could help me?", "What you can do?", "What help you provide?", "How you can be helpful?", "What support is offered"],
         "responses": ["I can answer your question like Introduce yourself, education, skills, internships, projects, Certifications, Extra Curricular Activities, Strengths, Contact Information, Resume, Achievements"],
         "context": [""]
        },
        {"tag": "introduction",
         "patterns": ["Introduce", "Introduce your self", "Tell me something about yourself","Tell me a bit about yourself.",
         "Mind sharing a little about who you are?",
         "Can you give me the quick version of your story?",
         "What's your story?",
         "Give me the lowdown on who you are." ,
         "Would you like to introduce yourself?",
         "Could you provide an introduction about yourself?",
         "I'd love to know more about you. Could you share a brief introduction?",
         "Could you give us some background information about yourself?",
         "Let's start by having you introduce yourself.",
         "Please take a moment to introduce yourself.",
         "We would appreciate it if you could provide a formal introduction.",
         "Kindly begin by introducing yourself and your background.",
         "As part of our formalities, we request you to introduce yourself.",
         "Could you present a concise introduction of who you are?",
         "Paint us a picture of who you are in a few words.",
         "Give us the 'elevator pitch' version of yourself.",
         "Sum up your awesomeness in a nutshell.",
         "If you were a book, what would the blurb say?",
         "Imagine your life as a movie trailer. How would you introduce yourself?"],
         "responses": ["I would Like to introduce myself, So, currently I'm a dedicated student in pursuit of a B.Tech degree in Artificial Intelligence and Data Science. My journey into the world of technology began with completing diplomas in Computer Engineering which triggered my passion for creating innovative solutions and exploring the potential of AI and DS. I believe that AI and Data Science are the driving forces behind groundbreaking advancements in various fields. I'm deeply inspired by the power of algorithms to analyze complex data and extract meaningful insights, enabling us to make informed decisions. From developing predictive models to uncovering hidden patterns, I find the challenges of this field both intellectually stimulating and practically impactful. In a rapidly evolving technological landscape, my aim is to keep learning, growing, and collaborating with like-minded individuals who share a similar passion for pushing the boundaries of AI and Data Science. I'm excited to connect, learn, and create alongside fellow enthusiasts on this remarkable journey."],
         "context": [""]
        },
        {"tag": "education",
         "patterns": ["Education", "Education background", "tell us about your education", 
         "Could you please provide an overview of your educational background?",
         "Tell me about your academic journey and the degrees you've earned.",
         "What institutions did you attend for your education?",
         "How do you feel your educational background prepares you for this role?",
         "In what ways has your education contributed to your skills and abilities for this position?",
         "Can you highlight how your academic experiences align with the requirements of this job?",
         "What is your current CGPA and SGPA",
         "Your academic qualifications" ],
         "responses": ["I completed my Schooling (SSC) from New English Medium Secondary School, with percentage of 79.60%. This early foundation laid the groundwork for my subsequent academic achievements.After that, I pursued a Diploma in Computer Engineering from All India Shri Shivaji Memorial Society, where I achieved remarkable success with a distinction and an outstanding percentage of 93.83%. This period allowed me to delve deep into the field of computer engineering and gain valuable practical knowledge.Currently, I am pursuing a B.Tech degree in Artificial Intelligence and Data Science from Vishwakarma Institute of Technology,Pune . I am proud to maintain a competitive CGPA of 8.33 and SGPA 8.09, reflecting my dedication to academic excellence and my passion for the dynamic field of AI and DS."],
         "context": [""]
        },  
        {"tag": "skills",
         "patterns": ["skills","tell me about your skills",
         "Could you provide an overview of your relevant skills?",
         "What skills do you believe make you a strong fit for this position?",
         "What are your core competencies that you think are valuable for this role?",
         "What technical skills do you possess that are directly relevant to this role?",
         "Can you walk us through your technical toolkit?",
         "In terms of technical abilities, what would you consider your strengths?",
         "Based on the job description, what skills of yours align with the role's requirements?",
         "How do your skills match the key responsibilities of this position?",
         "Which of your skills do you believe will contribute the most to the success of this role?"],
         "responses": ["Technical Skills: HTML (Advanced), WordPress (Advanced), Python (Advanced), Java (Intermediate), MySQL (Intermediate), Android (Intermediate), CSS (Intermediate), R Programming (Intermediate), Data Science (Intermediate), Artificial Intelligence (Intermediate), SQL (Intermediate), Power BI (Intermediate), PHP (Beginner), JavaScript (Beginner), REST API (Beginner) Language Proficiency: English Proficiency (Spoken - Advanced)"],
         "context": [""]
        },
        {"tag": "Internships",
         "patterns": ["internship","Internships","Have you done any internship",
         "Have you had any internship experiences?",
         "Could you share if you've been involved in any internships?",
         "Are there any internships you've participated in?",
         "Have you completed any internships in your field?",
         "Can you tell me about any internship opportunities you've pursued?",
         "Have you had the chance to gain practical experience through internships?",
         "Could you discuss any internships that have contributed to your professional development?"],
         "responses": ["Data Science Intern Oasis Infobyte, Virtual July 2023 - August 2023 During my internship at Oasis Infobyte, I had the opportunity to immerse myself in the world of Data Science. I engaged in data analysis on diverse datasets, crafting various prediction models to derive meaningful insights. My responsibilities included contributing to Exploratory Data Analysis, leveraging statistical techniques, and collaborating with the team to identify trends and patterns. This experience further fueled my passion for Data Science and provided hands-on exposure to real-world applications. Technical Content Writer Geeks for Geeks, Virtual April 2023 - July 2023 As a Technical Content Writer at Geeks for Geeks, I had the privilege of translating complex technical concepts into clear and concise articles. This role honed my ability to communicate intricate topics effectively to a wide audience. I meticulously researched and crafted informative pieces that contributed to the platform's repository of knowledge. This experience not only enhanced my technical writing skills but also solidified my understanding of various programming and computer science concepts. Proofreader Intern Samagra Foundation, Virtual November 2020 - December 2020 During my internship at Samagra Foundation, I served as a proofreader and took on the responsibility of reviewing and refining content with a keen eye for detail. Successfully completing my tasks before deadlines and earning a Letter of Recommendation reinforced my dedication to accuracy and timely delivery. This experience sharpened my proofreading abilities and provided me with a deeper appreciation for the importance of meticulous editing."],
         "context": [""]
        },
        {"tag": "Projects",
         "patterns": ["projects","Could you walk me through some of the projects you've worked on?",
         "Tell me about the projects you've been involved in.",
         "Can you describe a few of the key projects you've completed?",
         "I'd love to hear about the projects you've undertaken. Could you share a few?",
         "In terms of hands-on experience, could you provide an overview of the projects you've worked on?",
         "What kind of projects have you been a part of, and what were your roles and contributions?",
         "Projects often provide valuable insights into your skills. Could you elaborate on a few that you're particularly proud of?",
         "Share with us a few examples of projects that you've tackled in your career so far.",
         "When it comes to practical application, could you give us some details about the projects you've completed?",
         "Let's dive into your practical experience. Can you give me an idea of the types of projects you've been hands-on with?" ],
         "responses": ["Brain Stroke Prediction using Machine Learning December 2022 - January 2023 In this project, I undertook the task of predicting brain strokes using Machine Learning techniques. I utilized Ensemble Learning on a comprehensive brain stroke dataset, enabling accurate predictions. Furthermore, I innovatively assessed the severity of strokes, leading to the development of personalized exercise recommendations based on stroke severity. This project not only demonstrated the potential of Machine Learning in healthcare but also underscored the importance of data-driven insights in critical medical situations. Motion Palette Suite: Virtual Painter, Virtual Mouse, Virtual Keyboard August 2023 - Present As part of the Motion Palette Suite, I am actively involved in the creation of a revolutionary interaction paradigm for computer systems. This suite seamlessly integrates Virtual Painter, Virtual Mouse, and Virtual Keyboard functionalities, redefining user-computer interaction. I am utilizing cutting-edge technologies such as deep learning and neural networks to elevate the project's success. Through this endeavor, I am committed to shaping the future of Human-Computer Interaction by implementing innovative solutions that enhance user experience and accessibility."],
         "context": [""]
        },
        {"tag": "Certifications",
         "patterns": ["certificates","certificate","certifications","Have you pursued any certifications that are relevant to this role?",
         "Could you tell us about any certifications you've obtained?",
         "Are there any professional certifications you hold that you believe are valuable for this position?",
         "Can you share if you've earned any certifications that align with the skills needed for this job?",
         "What certifications do you have that you think make you a strong candidate for this role?",
         "Have you invested in any certifications to enhance your expertise in specific areas?",
         "Could you discuss any certifications you believe have contributed significantly to your skill set?",
         "Are there any certifications you've pursued to stay current in your field?",
         "Tell us about any certifications you hold that showcase your proficiency in certain technologies or practices.",
         "In terms of professional development, have you earned any certifications that you believe would benefit this position?" 
         ],
         "responses": ["Data Science- British Airways, Online Aug 2023  Aug 2023 Worked on Real Time airline data by web scrapping, and developed prediction models also performed Analysis to identify trends and patterns from the dataset. Artificial Intelligence- Cognizant, Online Jul 2023  Aug 2023 Worked on real time sales data and identified trends and patterns from the dataset also developed a sales prediction model on which any dataset could work."],
         "context": [""]
        },
        {"tag": "Extra-Curricular Activities",
         "patterns": ["activities other than academics","co-curricular activities","activities","activity","extra curricular activities","Beyond your professional experiences, are there any extracurricular activities you're involved in?",
         "Tell us about any activities you engage in outside of work that you're particularly passionate about.",
         "Are there any hobbies or interests you pursue outside of your career?",
         "Could you share any non-work activities that you believe have contributed to your personal growth?",
         "In addition to your professional endeavors, do you have any hobbies or activities that you enjoy?",
         "What do you like to do in your free time? Are there any activities that you find fulfilling?",
         "Are there any clubs, organizations, or hobbies that you're actively involved in?",
         "Tell us about any extracurricular pursuits that you think have enriched your skill set.",
         "Outside of work, how do you like to spend your time? Are there any hobbies you're passionate about?",
         "What are some of your interests or activities that help you unwind and recharge?"],
         "responses": ["Aesthetic Secretary - Event Planning and Education Committee (EPEC)- During my time as the Aesthetic Secretary of the Event Planning and Education Committee (EPEC), I actively contributed to the planning and execution of various events. This role allowed me to combine my organizational skills with creative thinking, as I worked closely with the team to ensure seamless and visually appealing event experiences. From ideation to execution, I embraced the challenge of harmonizing aesthetics and logistics to create memorable moments for attendees."],
         "context": [""]
        },
        {"tag": "Weekness",
         "patterns": ["strengths,weeknesses,weekness"],
         "responses": ["Strengths: One of my greatest strengths lies in my genuine passion for data science. I thrive on exploring data, uncovering patterns, and deriving meaningful insights that can drive informed decision-making. This passion fuels my motivation to continuously learn and adapt to the ever-evolving landscape of data science technologies and methodologies. Additionally, my analytical mindset allows me to approach complex problems with a structured and strategic perspective. I take pride in my ability to communicate these intricate insights effectively, bridging the gap between technical details and practical applications. Weaknesses: While my passion for data science is a significant strength, it can sometimes lead me to become deeply engrossed in a project, and I might find it challenging to step away. I'm aware that balance is crucial, and I'm actively working on maintaining a healthy separation between work and personal time. Moreover, due to the rapid advancements in data science, there's always more to learn. Occasionally, I can become too eager to explore every emerging technology, which might lead to feeling overwhelmed. To address this, I'm developing a focused learning plan to ensure I gain in-depth expertise in areas that align with my goals and the demands of the industry."],
         "context": ["What are your weekness?"]
        },
        {"tag": "Strengths",
         "patterns": ["strengths","weeknesses",
         "What do you consider your greatest strengths?",
         "Can you highlight some of your key strengths that you bring to a team?",
         "From your perspective, what strengths set you apart as a candidate for this role?",
        "In terms of your abilities, what strengths do you believe make you a strong fit for our company?",
        "What skills and qualities do you feel make you a valuable addition to our team?",
        "Could you share some of the strengths that you think align well with the requirements of this position?",
        "How would you describe your core strengths that contribute to your success?",
        "From your experiences, what strengths have consistently enabled you to excel?",
        "In terms of your professional attributes, what strengths have you developed that you believe are crucial for this role?",
        "What do you believe are the strengths that make you a well-rounded and effective professional?"
        ],
         "responses": ["Strengths: One of my greatest strengths lies in my genuine passion for data science. I thrive on exploring data, uncovering patterns, and deriving meaningful insights that can drive informed decision-making. This passion fuels my motivation to continuously learn and adapt to the ever-evolving landscape of data science technologies and methodologies. Additionally, my analytical mindset allows me to approach complex problems with a structured and strategic perspective. I take pride in my ability to communicate these intricate insights effectively, bridging the gap between technical details and practical applications. Weaknesses: While my passion for data science is a significant strength, it can sometimes lead me to become deeply engrossed in a project, and I might find it challenging to step away. I'm aware that balance is crucial, and I'm actively working on maintaining a healthy separation between work and personal time. Moreover, due to the rapid advancements in data science, there's always more to learn. Occasionally, I can become too eager to explore every emerging technology, which might lead to feeling overwhelmed. To address this, I'm developing a focused learning plan to ensure I gain in-depth expertise in areas that align with my goals and the demands of the industry."],
         "context": [""]
        },
        {"tag": "hobbies",
         "patterns": ["What hobbies do you enjoy in your free time?",
         "Could you share a hobby you're passionate about?",
         "How have your hobbies contributed to your personal growth?",
         "Have any of your hobbies taught you important life lessons?",
         "Can you provide an example of a collaborative aspect in one of your hobbies?",
         "Have your hobbies ever influenced your career choices?",
         "How do you balance your hobbies and work responsibilities?",
         "Which hobbies do you find most relaxing after a challenging day?",
         "Can you discuss a hobby that showcases your creativity?",
         "Do you see any connections between your hobbies and the qualities needed for this role?"],
         "responses": ["My hobbies are drawing, painting and sketching. They bring a creative edge to data science by providing me visualization skills in creating impactful data visualizations. Experience in problem-solving and attention to detail in artistic work translates to identifying patterns in data. Patience honed through artistic practice is invaluable during complex data analysis, and ability to convey stories visually complements data storytelling. Additionally, cross-disciplinary thinking showcases a unique approach to problem-solving, his sets me as a well-rounded data scientist."],
         "context": [""]
        },
        {"tag": "achievements",
        "patterns": ["Could you share some of your notable achievements from your academic or professional journey?",
        "What accomplishments are you most proud of in your career so far?",
        "Can you highlight any achievements that you believe demonstrate your strengths and skills?",
        "Have you received any awards or recognition for your work? If so, could you tell us about them?",
        "Are there specific projects or initiatives where you've achieved exceptional results?",
        "Can you discuss a time when you overcame a significant challenge and achieved a positive outcome?",
        "Have you led any projects that had a notable impact on your team or organization?",
        "Could you provide examples of achievements that highlight your leadership or teamwork skills?",
        "What achievements do you feel have contributed most to your professional growth?",
        "Are there any accomplishments you've achieved that demonstrate your ability to adapt and learn quickly?"],
        "responses": ["During my pursuit of a Diploma in Computer Engineering, I achieved the status of institute topper, showcasing my consistent dedication and academic excellence. In addition, I was recognized as the Best Student of the Year during my school years, affirming not only my strong academic performance but also my well-rounded contributions to the school community."],
        "context": [""]
       },
       
        {"tag": "Contact Information",
        "patterns": ["how can we connect",
        "contact","contact information"," ","connect",
            "What's the best way to reach out to you for further communication?",
        "Could you share your preferred contact details for us to stay in touch?",
        "How would you like us to connect with you after the interview process?",
        "Are you comfortable sharing your preferred method of communication?",
        "Can you let us know how you'd prefer us to reach you for any follow-up?",
        "Would you be open to sharing your contact information so we can continue the conversation?",
        "What communication channels do you use regularly and are comfortable sharing with us?",
        "Are there specific email or phone details you'd like us to use for further discussions?",
        "Is there a preferred method through which we can keep you updated on the interview process?",
        "Do you have any preferences for how we can stay connected throughout the hiring process?"],
        "responses": ["Email Id- shravanimjagtap13@gmail.com, LinkedIn-https://www.linkedin.com/in/shravani-jagtap-4845761ba, Github-https://github.com/Shravani1383, Blog-https://auth.geeksforgeeks.org/user/shravanimjagtap13/articles"],
        "context": [""]
       }
   ]
}

def get_response(intent_tag):
    intent = next((item for item in data["intents"] if item["tag"] == intent_tag), None)
    if intent:
        return random.choice(intent["responses"])
    else:
        return "I'm sorry, I couldn't find an appropriate response."
    
def preprocess_text(text):
    # Tokenize the input text
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    return lemmatized_tokens

def calculate_similarity(user_tokens, pattern_tokens):
    if not user_tokens or not pattern_tokens:
        return 0
    common_tokens = set(user_tokens).intersection(pattern_tokens)
    similarity = len(common_tokens) / max(len(user_tokens), len(pattern_tokens))
    return similarity

def get_best_matching_intent(user_input):
    user_tokens = preprocess_text(user_input)
    best_similarity = 0
    best_intent = None
    
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            pattern_tokens = preprocess_text(pattern)
            similarity = calculate_similarity(user_tokens, pattern_tokens)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_intent = intent
    
    return best_intent

def main():
    print("Shravani's Chatbot: Hello! How can I assist you today?")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Shravani's Chatbot: Goodbye! Feel free to reach out anytime.")
            break
        
        best_intent = get_best_matching_intent(user_input)
        if best_intent and best_intent["tag"] != "noanswer":
            print("Shravani's Chatbot:", get_response(best_intent["tag"]))
        else:
            print("Shravani's Chatbot:", get_response("noanswer"))
            
if __name__ == "__main__":
    main()
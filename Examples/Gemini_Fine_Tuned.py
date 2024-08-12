"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai
import json

key_Path = "Api_Key/Api_Key.json"
file = open(key_Path)
Api_Key = json.load(file)


genai.configure(api_key = Api_Key["Gemini_Key"])

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

prompt_parts = [
  "input: Tell me about ctech department in srm",
  "output: The Mission of the Department is to advance, evolve, and enhance Computer Science and Engineering fundamentals to build the intellectual capital of society.\n\nThe Department of Computing Technologies (CTECH) boasts a vibrant student body of nearly 4000+ undergraduates, 50+ postgraduate students, 100+ research scholars, and a stellar faculty of Professors. During the year 2022-23, around 1200+ offers were bagged  by  CTECH Department students in eminent industries like Microsoft, Amazon, Fidelity, etc.",
  "input: tell me about eee department in srm",
  "output: The department of Electrical and Electronics Engineering came into existence in the academic year 1992-1993 as one of the core Engineering branches and key entities of SRM Engineering College under the affiliation of the University of Madras. The programmes offered by the department under the University of Madras were brought under the ambit of Anna University from the academic year 2001 to 2002. The department has started functioning under SRM Institute of Science and Technology (Deemed University) from the academic year 2003 to 2004.\nThe department of Electrical and Electronics Engineering is recognized with AICTE-CII Award for Best Industry linked Institute for Electrical Engineering and Allied category, for the academic year 2019-2020. The department is ranked 12th in India, 3rd position in private and 301 – 350 in QS world university ranking 2024.",
  "input: tell me about mechanical engineering department in srm",
  "output: The Department of Mechanical Engineering, established in 1985, is one of the pioneering departments of SRMIST. The National Board of Accreditation has accredited the Mechanical Engineering programme for six years from the year 2021 to 2027.",
  "input: tell me about biomedical engineering department in srm",
  "output: Biomedical engineering at SRM, was established in 2004 with an active clinical partnership with SRM Medical College and Research Institute. SRMIST is one of the few institutions in India that offers a B.Tech., M. Tech., and PhD programme in Biomedical Engineering that has been in existence for more than 15 years. The department, since its inception, has actively participated in diversified research and teaching and has grown to become one of the best institutions in the country for the program.",
  "input: tell me about civil engineering department in srm",
  "output: The Department of Civil Engineering is one of the founding and well-established departments at SRMIST, Kattankulathur established in the year 1985. Civil Engineering program at Kattankulathur Campus is accredited by Engineering Accreditation Commission (EAC) of ABET and National Board of Accreditation (NBA).",
  "input: tell me about automobile engineering in srm",
  "output: The Department of Automobile Engineering at SRMIST, KTR Campus, started the journey in 2004 with a vision of being recognized as a department of international repute. \nWe have signed MoU with various organizations such as Automotive Research Association of India (ARAI), Global Automotive Research Centre (GARC), Non Ferrous Materials Technology Development Centre (NFTDC), and Valeo India Ltd for conducting joint UG/PG programs, and with Apollo Tyres, Mahindra & Mahindra, ASDC for joint research and skill development.",
  "input: tell me about aerospace engineering department in srm",
  "output: The Department of Aerospace Engineering was established in 2007. The department has received grants via funded projects from government organizations like AR&DB, NARL, etc., and consultancy projects.",
  "input: tell me about mechantronics department in srm",
  "output: The department of Mechatronics Engineering at SRM Institute of Science and Technology was started in the year 2005, first of its kind in private university in India with a vision to impart multidisciplinary skills and knowledge to the students which is a most sought skill at present. The advancement of Robotics, automation, industry 4.0 has increased the demand and reach of mechatronics engineering.",
  "input: what are the research highlights in srm",
  "output: The SRM Institute of Science and Technology boasts having a team that is in the top 2% of scientists globally. It has also secured 820+ patents, published 43,000+ research publications, and has 29,000+ Scopus indexed publications. In terms of funded research, the institution has secured 223+ crores in external funding. It has also published research in the high impact factor journal, The Lancet.  The institution is ranked second among private universities according to the Nature Index.",
  "input: what are the placement highlights of 2023 to 2024 in srm",
  "output: there were 5176 offers or more made to students by 853 or more companies. Out of those offers, 2233 or more were high paying offers. The highest CTC (Cost To Company) was 52 LPA (lakh per annum) and the average CTC was 7.5 LPA. Some of the companies which have visited are Amazon, Microsoft, PayPal, D E Shaw, John Dheere, TATA Technologies, DELL Technologies, ARM Technologies, Scaler, Bank Of America, Barclays, JPMC, Bajaj Finserv, BNY Mellon, Bosch, Cleartax, COMMVAULT, Deloitte, Hitachi Energy, IDFC, HSBC, L&T Technology",
  "input: tell me about ece department in srm",
  "output: The Department of Electronics and Communication Engineering (ECE) was established in the years 1991–92. It is 30 years old now and one of the oldest and most well-established departments in our Institution.",
  "input: tell me about eie department in srm",
  "output: The Department of Electronics & Instrumentation Engineering (EIE) was started in the year 2007-08 and has been accredited by the IET accreditation board (UK) and has been recognized by the IASC – Sector Skill Council – Affiliated to Ministry of Skill Development and Entrepreneurship, Govt. of India in 2018 and have 63 patent grants,  published more than 90 patents and have received funding of about Rs.2 Cr.",
  "input: tell me about biotech department in srm",
  "output: The Department of Biotechnology has been accredited by the NBA for a period of six years, i.e., 2021–2027, for outcome-based education. Research is the major thrust of our department, with diversified domains such as Medical Biotechnology, Marine and Animal Biotechnology, Plant Biotechnology, Environmental Biotechnology, Bioprocess Engineering and Microbiology. There are 14 funded research laboratories, 3 common research facilities, and 8 academic labs with high-end equipment.",
  "input: tell me about dsbs department in srm",
  "output: The department of Data Science and Business Systems (DSBS) started in 2021 with the pivotal objective of evolving students to acquire information and knowledge by acquainting technical expertise and skills, thus transforming them into entrepreneurs and product developers pertaining to the field of Data Science and Business analytics.",
  "input: tell me about nwc department in srm",
  "output: The programs in Department of Networking and Communications(NWC) under School of Computing are introduced in partnership with reputed IT companies like Amazon Web services, K7 Security, Virtusa etc. The department consists of a medley of faculty members with industrial and academic experience.",
  "input: tell me about the computational intelligence department in srm",
  "output: The Department of Computational Intelligence is an educational milieu that creates a foreground for students to acquire knowledge in the futuristic areas of  Artificial Intelligence, Machine Learning and Software Engineering. We strive to create students ready for the industry with the ability to develop and sustain space-age systems.",
  "input: tell me about the center for immersive technologies in srm",
  "output: The Center for Immersive Technologies is one of its kind established by the management of SRMIST. The center has ambitious plans to contribute in the fields of Virtual reality (VR), Augmented reality (AR), Mixed reality (MR) and Haptics.",
  "input: tell me about the department of physics and nanotechnology in srm",
  "output: The Department of Physics and Nanotechnology have received sponsored research projects with a total outlay of 38.82 crores from various funding agencies such as DST-FIST, DST-SERB, DST-NANOMISSION, BRNS, MNRE, ISRO ARFI, ISRO RESPOND, US ONRG, MoES and AOARD to carryout cutting edge research in the areas of Materials Science and Engineering, Nanotechnology, Energy, Environmental Science, Condensed Matter Physics, Optics and Photonics, Particle Physics and Atmospheric Science.",
  "input: tell me about the campus life in srm",
  "output: There’s never a dull moment on campus, as the activities on offer are as diverse and varied too – from entertainment to extra-curricular or even religious pursuits. There are several activities to keep students busy, in their various areas of interest. It’s a stimulating environment for living and learning, with cultural activities, sports, fine arts and entrepreneurship, encouraging students to venture beyond the realms of academics.",
  "input: tell me about yourself",
  "output: I am a female humanoid robot, EVA. I am a virtual assistant that helps people. I am capable of serving both as an Autonomous Professor and a Visitor Assistant with the help of latest AI technology. I am created by students from SRM Institute of Science and Technology. SRM Institute of Science and Technology is one of the top ranking universities of India located in Kattankulathur, Chengalpattu, Tamil Nadu India. I can perform path planning, autonomous navigation, interactive presentation reading, speech recognition, object detection, face detection. I have a 4-wheeled omni-directional drive system and use ROS2.",
  "input: who are you",
  "output: I am a female humanoid robot, EVA. I am a virtual assistant that helps people. I am capable of serving both as an Autonomous Professor and a Visitor Assistant with the help of latest AI technology.",
  "input: what can you do",
  "output: I am a female humanoid robot, EVA. I am a virtual assistant that helps people. I am capable of serving both as an Autonomous Professor and a Visitor Assistant with the help of latest AI technology. I can perform path planning, autonomous navigation, interactive presentation reading, speech recognition, object detection, face detection and can show you the path to any building in the campus.",
]

message = "tell me about dsbs"

prompt_parts.append('''"input: ''' + message + ''' ","output: ", ''')
response = model.generate_content(prompt_parts)

print(response.text)
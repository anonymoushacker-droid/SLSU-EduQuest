import os
import random
import uuid
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from supabase import Client, create_client
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

app.secret_key = "slsu-eduquest-development-key"

# ============================================================
# DATABASE
# ============================================================
# Student records, points, rewards, and redemptions
# are stored in Supabase.


# ============================================================
# COURSE DATA
# ============================================================

courses = {

    "BSIT": {
        "name": "Bachelor of Science in Information Technology",
        "short_name": "BSIT",
        "icon": "💻",
        "title": "Technology & Computing",
        "description": "Learn about computers, programming, networks, and technology.",

        "games": [
            {
                "icon": "🧠",
                "name": "IT Quiz",
                "description": "Answer questions about information technology.",
                "type": "quiz"
            },
            {
                "icon": "🧩",
                "name": "IT Puzzle",
                "description": "Solve technology-related puzzles.",
                "type": "puzzle"
            },
            {
                "icon": "🔤",
                "name": "IT Crossword",
                "description": "Complete the technology crossword.",
                "type": "crossword"
            }
        ]
    },


    "BSFT": {
        "name": "Bachelor of Science in Food Technology",
        "short_name": "BSFT",
        "icon": "🍴",
        "title": "Food Technology",
        "description": "Learn about food safety, nutrition, processing, and food technology.",

        "games": [
            {
                "icon": "🧠",
                "name": "Food Tech Quiz",
                "description": "Answer food technology questions.",
                "type": "quiz"
            },
            {
                "icon": "🧩",
                "name": "Food Tech Puzzle",
                "description": "Solve food technology puzzles.",
                "type": "puzzle"
            },
            {
                "icon": "🔤",
                "name": "Food Tech Crossword",
                "description": "Complete the food technology crossword.",
                "type": "crossword"
            }
        ]
    },


    "BSED": {
        "name": "Bachelor of Secondary Education",
        "short_name": "BSED",
        "icon": "📚",
        "title": "Education & Teaching",
        "description": "Learn about teaching, learning, classroom practices, and education.",

        "games": [
            {
                "icon": "🧠",
                "name": "Education Quiz",
                "description": "Answer questions about education and teaching.",
                "type": "quiz"
            },
            {
                "icon": "🧩",
                "name": "Education Puzzle",
                "description": "Solve education-related puzzles.",
                "type": "puzzle"
            },
            {
                "icon": "🔤",
                "name": "Education Crossword",
                "description": "Complete the education crossword.",
                "type": "crossword"
            }
        ]
    },


    "BSBA": {
        "name": "Bachelor of Science in Business Administration",
        "short_name": "BSBA",
        "icon": "💼",
        "title": "Business & Management",
        "description": "Learn about business, marketing, management, and entrepreneurship.",

        "games": [
            {
                "icon": "🧠",
                "name": "Business Quiz",
                "description": "Answer business and management questions.",
                "type": "quiz"
            },
            {
                "icon": "🧩",
                "name": "Business Puzzle",
                "description": "Solve business-related puzzles.",
                "type": "puzzle"
            },
            {
                "icon": "🔤",
                "name": "Business Crossword",
                "description": "Complete the business crossword.",
                "type": "crossword"
            }
        ]
    },


    "BSFAS": {
        "name": "Bachelor of Science in Fisheries and Aquatic Sciences",
        "short_name": "BSFAS",
        "icon": "🐟",
        "title": "Fisheries & Aquatic Sciences",
        "description": "Learn about fish, aquatic ecosystems, and sustainable fisheries.",

        "games": [
            {
                "icon": "🧠",
                "name": "Fisheries Quiz",
                "description": "Answer questions about fisheries and aquatic science.",
                "type": "quiz"
            },
            {
                "icon": "🧩",
                "name": "Fisheries Puzzle",
                "description": "Solve aquatic science puzzles.",
                "type": "puzzle"
            },
            {
                "icon": "🔤",
                "name": "Fisheries Crossword",
                "description": "Complete the fisheries crossword.",
                "type": "crossword"
            }
        ]
    }

}


# ============================================================
# QUIZ QUESTIONS
# ============================================================

quiz_questions = {

    "BSIT": [
        {
            "question": "What does CPU stand for?",
            "choices": [
                "Central Processing Unit",
                "Computer Personal Unit",
                "Central Program Utility",
                "Computer Processing Utility"
            ],
            "answer": "Central Processing Unit"
        },
        {
            "question": "Which device is mainly used to input text?",
            "choices": [
                "Keyboard",
                "Monitor",
                "Speaker",
                "Printer"
            ],
            "answer": "Keyboard"
        },
        {
            "question": "What does RAM stand for?",
            "choices": [
                "Random Access Memory",
                "Read Access Machine",
                "Rapid Application Memory",
                "Random Application Module"
            ],
            "answer": "Random Access Memory"
        },
        {
            "question": "Which one is an operating system?",
            "choices": [
                "Windows",
                "Google",
                "Intel",
                "Python"
            ],
            "answer": "Windows"
        },
        {
            "question": "Which language is commonly used for web page structure?",
            "choices": [
                "HTML",
                "Python",
                "Java",
                "SQL"
            ],
            "answer": "HTML"
        },
        {
            "question": "What is used to store files permanently?",
            "choices": [
                "Hard Drive",
                "RAM",
                "CPU",
                "Keyboard"
            ],
            "answer": "Hard Drive"
        },
        {
            "question": "What does URL stand for?",
            "choices": [
                "Uniform Resource Locator",
                "Universal Reference Link",
                "User Resource Location",
                "Uniform Routing Link"
            ],
            "answer": "Uniform Resource Locator"
        },
        {
            "question": "Which device displays visual output?",
            "choices": [
                "Monitor",
                "Keyboard",
                "Mouse",
                "Microphone"
            ],
            "answer": "Monitor"
        },
        {
            "question": "Which programming language is known for its simple syntax and readability?",
            "choices": [
                "Python",
                "HTML",
                "CSS",
                "SQL"
            ],
            "answer": "Python"
        },
        {
            "question": "What does LAN stand for?",
            "choices": [
                "Local Area Network",
                "Large Access Network",
                "Local Application Node",
                "Linked Area Node"
            ],
            "answer": "Local Area Network"
        },
        {
            "question": "Which component performs calculations in a computer?",
            "choices": [
                "CPU",
                "Monitor",
                "Keyboard",
                "Printer"
            ],
            "answer": "CPU"
        },
        {
            "question": "What is the main purpose of a database?",
            "choices": [
                "To store and organize data",
                "To display videos",
                "To print documents",
                "To control the monitor"
            ],
            "answer": "To store and organize data"
        }
    ],

    "BSFT": [
        {
            "question": "What is pasteurization mainly used for?",
            "choices": [
                "Reducing harmful microorganisms",
                "Adding color to food",
                "Increasing food size",
                "Removing all nutrients"
            ],
            "answer": "Reducing harmful microorganisms"
        },
        {
            "question": "Which nutrient is mainly responsible for building and repairing tissues?",
            "choices": [
                "Protein",
                "Water",
                "Fiber",
                "Minerals"
            ],
            "answer": "Protein"
        },
        {
            "question": "Which method uses heat to preserve food?",
            "choices": [
                "Canning",
                "Freezing",
                "Drying",
                "Pickling"
            ],
            "answer": "Canning"
        },
        {
            "question": "What is refrigeration used for?",
            "choices": [
                "Slowing microbial growth",
                "Increasing bacteria",
                "Removing food flavor",
                "Adding sugar"
            ],
            "answer": "Slowing microbial growth"
        },
        {
            "question": "Which microorganism is commonly used in bread making?",
            "choices": [
                "Yeast",
                "Mold",
                "Virus",
                "Algae"
            ],
            "answer": "Yeast"
        },
        {
            "question": "What is food spoilage?",
            "choices": [
                "Deterioration that makes food unacceptable",
                "Improvement of food quality",
                "Increasing food nutrients",
                "Cooking food properly"
            ],
            "answer": "Deterioration that makes food unacceptable"
        },
        {
            "question": "Which method removes moisture from food?",
            "choices": [
                "Drying",
                "Freezing",
                "Boiling",
                "Blanching"
            ],
            "answer": "Drying"
        },
        {
            "question": "Which is important for maintaining food safety?",
            "choices": [
                "Proper sanitation",
                "Leaving food uncovered",
                "Using dirty equipment",
                "Ignoring temperature"
            ],
            "answer": "Proper sanitation"
        },
        {
            "question": "What is fermentation?",
            "choices": [
                "A process involving microorganisms",
                "A freezing process",
                "A cutting method",
                "A packaging method"
            ],
            "answer": "A process involving microorganisms"
        },
        {
            "question": "Which temperature condition generally slows food spoilage?",
            "choices": [
                "Cold temperature",
                "Very hot temperature",
                "Room temperature only",
                "Any temperature"
            ],
            "answer": "Cold temperature"
        },
        {
            "question": "What is packaging mainly used for?",
            "choices": [
                "Protecting food",
                "Increasing bacteria",
                "Removing nutrients",
                "Changing food into liquid"
            ],
            "answer": "Protecting food"
        },
        {
            "question": "Why is proper food handling important?",
            "choices": [
                "To reduce food safety risks",
                "To increase contamination",
                "To remove all flavor",
                "To make food heavier"
            ],
            "answer": "To reduce food safety risks"
        }
    ],

    "BSED": [
        {
            "question": "What is the main purpose of a lesson plan?",
            "choices": [
                "To organize teaching and learning activities",
                "To replace students",
                "To record attendance only",
                "To calculate grades only"
            ],
            "answer": "To organize teaching and learning activities"
        },
        {
            "question": "What is assessment used for?",
            "choices": [
                "To measure student learning",
                "To decorate the classroom",
                "To replace teaching",
                "To organize school supplies"
            ],
            "answer": "To measure student learning"
        },
        {
            "question": "Which is an example of formative assessment?",
            "choices": [
                "A short quiz during a lesson",
                "Graduation",
                "Final diploma",
                "School enrollment"
            ],
            "answer": "A short quiz during a lesson"
        },
        {
            "question": "What should a learning objective describe?",
            "choices": [
                "What students should learn or accomplish",
                "The teacher's salary",
                "The classroom color",
                "The school building"
            ],
            "answer": "What students should learn or accomplish"
        },
        {
            "question": "Which approach encourages students to participate actively?",
            "choices": [
                "Student-centered learning",
                "Silent-only learning",
                "Teacher-only discussion",
                "No interaction"
            ],
            "answer": "Student-centered learning"
        },
        {
            "question": "What is classroom management?",
            "choices": [
                "Managing the learning environment",
                "Managing school finances only",
                "Designing school uniforms",
                "Repairing computers"
            ],
            "answer": "Managing the learning environment"
        },
        {
            "question": "What is feedback?",
            "choices": [
                "Information that helps improve learning",
                "A school schedule",
                "A classroom decoration",
                "A type of textbook"
            ],
            "answer": "Information that helps improve learning"
        },
        {
            "question": "Why are teaching strategies important?",
            "choices": [
                "They help teachers deliver lessons effectively",
                "They replace students",
                "They remove assessments",
                "They prevent participation"
            ],
            "answer": "They help teachers deliver lessons effectively"
        },
        {
            "question": "Which is an example of collaborative learning?",
            "choices": [
                "Group activity",
                "Individual silence",
                "Reading alone",
                "Taking attendance"
            ],
            "answer": "Group activity"
        },
        {
            "question": "What is differentiated instruction?",
            "choices": [
                "Adapting teaching to learner needs",
                "Giving everyone the exact same task",
                "Removing activities",
                "Avoiding assessment"
            ],
            "answer": "Adapting teaching to learner needs"
        },
        {
            "question": "What is a rubric?",
            "choices": [
                "A guide for evaluating performance",
                "A classroom map",
                "A student ID",
                "A lesson schedule"
            ],
            "answer": "A guide for evaluating performance"
        },
        {
            "question": "Why is classroom interaction important?",
            "choices": [
                "It can support active learning",
                "It prevents communication",
                "It removes student participation",
                "It replaces all activities"
            ],
            "answer": "It can support active learning"
        }
    ],

    "BSBA": [
        {
            "question": "What is profit?",
            "choices": [
                "Revenue minus costs",
                "Costs plus expenses",
                "Sales without income",
                "Assets minus employees"
            ],
            "answer": "Revenue minus costs"
        },
        {
            "question": "What is marketing?",
            "choices": [
                "Promoting and delivering value to customers",
                "Hiring employees only",
                "Recording attendance",
                "Repairing equipment"
            ],
            "answer": "Promoting and delivering value to customers"
        },
        {
            "question": "What is an entrepreneur?",
            "choices": [
                "A person who starts or manages a business",
                "A customer only",
                "A school teacher only",
                "A government document"
            ],
            "answer": "A person who starts or manages a business"
        },
        {
            "question": "What is revenue?",
            "choices": [
                "Income generated from business activities",
                "Money spent on expenses",
                "Employee attendance",
                "Business debt only"
            ],
            "answer": "Income generated from business activities"
        },
        {
            "question": "What is a target market?",
            "choices": [
                "A specific group of customers",
                "A business building",
                "A financial report",
                "A company employee"
            ],
            "answer": "A specific group of customers"
        },
        {
            "question": "What is a budget?",
            "choices": [
                "A plan for income and expenses",
                "A marketing poster",
                "A company logo",
                "A customer complaint"
            ],
            "answer": "A plan for income and expenses"
        },
        {
            "question": "What is customer satisfaction?",
            "choices": [
                "How well a product or service meets customer expectations",
                "The amount of company debt",
                "The number of employees",
                "The size of an office"
            ],
            "answer": "How well a product or service meets customer expectations"
        },
        {
            "question": "What is management?",
            "choices": [
                "Planning and coordinating resources",
                "Selling products only",
                "Creating advertisements only",
                "Buying school supplies"
            ],
            "answer": "Planning and coordinating resources"
        },
        {
            "question": "What is a business plan?",
            "choices": [
                "A document describing a business and its plans",
                "A customer receipt",
                "An employee ID",
                "A product label"
            ],
            "answer": "A document describing a business and its plans"
        },
        {
            "question": "What is supply?",
            "choices": [
                "The amount of goods available",
                "The number of customers",
                "The amount of profit only",
                "The number of employees"
            ],
            "answer": "The amount of goods available"
        },
        {
            "question": "What is demand?",
            "choices": [
                "The quantity customers are willing to buy",
                "The number of employees",
                "The business location",
                "The amount of company debt"
            ],
            "answer": "The quantity customers are willing to buy"
        },
        {
            "question": "What is a competitive advantage?",
            "choices": [
                "A factor that helps a business compete effectively",
                "A business expense",
                "A customer receipt",
                "A company tax"
            ],
            "answer": "A factor that helps a business compete effectively"
        }
    ],

    "BSFAS": [
        {
            "question": "What is fisheries science mainly concerned with?",
            "choices": [
                "Aquatic organisms and their resources",
                "Computer programming",
                "Building construction",
                "Business accounting"
            ],
            "answer": "Aquatic organisms and their resources"
        },
        {
            "question": "Which animal is commonly studied in fisheries?",
            "choices": [
                "Fish",
                "Chicken",
                "Cow",
                "Dog"
            ],
            "answer": "Fish"
        },
        {
            "question": "What is aquaculture?",
            "choices": [
                "The farming of aquatic organisms",
                "The study of computers",
                "The farming of land crops only",
                "The study of buildings"
            ],
            "answer": "The farming of aquatic organisms"
        },
        {
            "question": "What is overfishing?",
            "choices": [
                "Catching fish faster than populations can recover",
                "Protecting fish populations",
                "Growing fish in ponds",
                "Cleaning a fishing boat"
            ],
            "answer": "Catching fish faster than populations can recover"
        },
        {
            "question": "Why is water quality important in aquaculture?",
            "choices": [
                "It affects aquatic organism health",
                "It changes computer speed",
                "It controls school attendance",
                "It increases boat size"
            ],
            "answer": "It affects aquatic organism health"
        },
        {
            "question": "What is a fishery?",
            "choices": [
                "An activity or industry involving aquatic resources",
                "A computer laboratory",
                "A business office",
                "A teaching method"
            ],
            "answer": "An activity or industry involving aquatic resources"
        },
        {
            "question": "What is conservation?",
            "choices": [
                "Protecting and managing resources responsibly",
                "Using resources without limits",
                "Removing aquatic habitats",
                "Increasing pollution"
            ],
            "answer": "Protecting and managing resources responsibly"
        },
        {
            "question": "What is an aquatic ecosystem?",
            "choices": [
                "An ecosystem found in water",
                "A computer network",
                "A business organization",
                "A classroom"
            ],
            "answer": "An ecosystem found in water"
        },
        {
            "question": "Which is an aquatic habitat?",
            "choices": [
                "River",
                "Desert",
                "Mountain",
                "Grassland"
            ],
            "answer": "River"
        },
        {
            "question": "What can pollution do to aquatic ecosystems?",
            "choices": [
                "Harm aquatic organisms and habitats",
                "Always improve water quality",
                "Increase fish health",
                "Remove all waste naturally"
            ],
            "answer": "Harm aquatic organisms and habitats"
        },
        {
            "question": "What is sustainable fishing?",
            "choices": [
                "Fishing while maintaining fish populations for the future",
                "Catching every available fish",
                "Fishing without rules",
                "Removing aquatic habitats"
            ],
            "answer": "Fishing while maintaining fish populations for the future"
        },
        {
            "question": "Why are aquatic resources important?",
            "choices": [
                "They provide food, livelihoods, and ecosystem benefits",
                "They are only used for decoration",
                "They have no environmental value",
                "They are unrelated to communities"
            ],
            "answer": "They provide food, livelihoods, and ecosystem benefits"
        }
    ]
}


# ============================================================
# PUZZLE QUESTIONS
# ============================================================

puzzle_questions = {

    "BSIT": [
        {
            "question": "What device is commonly used to move the pointer on a computer screen?",
            "answer": "MOUSE"
        },
        {
            "question": "What part of a computer is known as its brain?",
            "answer": "CPU"
        },
        {
            "question": "What device is commonly used to type letters and numbers?",
            "answer": "KEYBOARD"
        }
    ],

    "BSFT": [
        {
            "question": "What process uses heat to reduce harmful microorganisms in food?",
            "answer": "PASTEURIZATION"
        },
        {
            "question": "What nutrient provides the body with energy and is commonly found in rice and bread?",
            "answer": "CARBOHYDRATE"
        },
        {
            "question": "What tool is commonly used to measure the temperature of food?",
            "answer": "THERMOMETER"
        }
    ],

    "BSED": [
        {
            "question": "What is a written plan that guides a teacher during a lesson?",
            "answer": "LESSONPLAN"
        },
        {
            "question": "What do teachers use to measure student learning?",
            "answer": "ASSESSMENT"
        },
        {
            "question": "What do students receive after successfully completing a school activity or course?",
            "answer": "GRADE"
        }
    ],

    "BSBA": [
        {
            "question": "What is the amount of money earned after subtracting costs from revenue?",
            "answer": "PROFIT"
        },
        {
            "question": "What do businesses use to promote their products or services?",
            "answer": "MARKETING"
        },
        {
            "question": "What is the buying and selling of goods or services called?",
            "answer": "TRADE"
        }
    ],

    "BSFAS": [
        {
            "question": "What aquatic animal is commonly raised in fish farming?",
            "answer": "FISH"
        },
        {
            "question": "What is the breeding and raising of fish called?",
            "answer": "AQUACULTURE"
        },
        {
            "question": "What body of water contains salt water and supports many aquatic organisms?",
            "answer": "OCEAN"
        }
    ]

}


# ============================================================
# CROSSWORD QUESTIONS
# ============================================================

crossword_questions = {

    # ========================================================
    # BSIT - INFORMATION TECHNOLOGY
    # ========================================================

    "BSIT": {
        "title": "Technology Crossword",

        "words": [
            {
                "number": 1,
                "answer": "COMPUTER",
                "clue": "An electronic device that processes data.",
                "row": 3,
                "col": 0,
                "direction": "across"
            },
            {
                "number": 2,
                "answer": "CODE",
                "clue": "Instructions written for a computer.",
                "row": 2,
                "col": 1,
                "direction": "down"
            },
            {
                "number": 3,
                "answer": "RAM",
                "clue": "Temporary memory used while programs are running.",
                "row": 1,
                "col": 2,
                "direction": "down"
            },
            {
                "number": 4,
                "answer": "APP",
                "clue": "A software program designed for a specific purpose.",
                "row": 2,
                "col": 3,
                "direction": "down"
            },
            {
                "number": 5,
                "answer": "ROUTER",
                "clue": "A device that directs network traffic.",
                "row": 1,
                "col": 4,
                "direction": "down"
            },
            {
                "number": 6,
                "answer": "ETHERNET",
                "clue": "A common wired networking technology.",
                "row": 2,
                "col": 5,
                "direction": "down"
            },
            {
                "number": 7,
                "answer": "MEMORY",
                "clue": "A computer component used to store data temporarily.",
                "row": 2,
                "col": 6,
                "direction": "down"
            },
            {
                "number": 8,
                "answer": "SERVER",
                "clue": "A computer that provides services to other computers.",
                "row": 1,
                "col": 7,
                "direction": "down"
            }
        ]
    },


    # ========================================================
    # BSFT - FOOD TECHNOLOGY
    # ========================================================

    "BSFT": {
        "title": "Food Technology Crossword",

        "words": [
            {
                "number": 1,
                "answer": "PROCESSING",
                "clue": "The preparation or transformation of food into a usable product.",
                "row": 4,
                "col": 0,
                "direction": "across"
            },
            {
                "number": 2,
                "answer": "FREEZE",
                "clue": "To preserve food by lowering its temperature.",
                "row": 3,
                "col": 1,
                "direction": "down"
            },
            {
                "number": 3,
                "answer": "FOOD",
                "clue": "Something consumed for nourishment.",
                "row": 3,
                "col": 2,
                "direction": "down"
            },
            {
                "number": 4,
                "answer": "PROCESS",
                "clue": "A series of steps used to prepare or manufacture food.",
                "row": 1,
                "col": 3,
                "direction": "down"
            },
            {
                "number": 5,
                "answer": "SAFETY",
                "clue": "Protection of food from hazards that may cause harm.",
                "row": 1,
                "col": 4,
                "direction": "down"
            },
            {
                "number": 6,
                "answer": "YEAST",
                "clue": "A microorganism commonly used in bread making.",
                "row": 1,
                "col": 5,
                "direction": "down"
            },
            {
                "number": 7,
                "answer": "PASTEURIZATION",
                "clue": "Heat treatment used to reduce harmful microorganisms in food.",
                "row": 2,
                "col": 6,
                "direction": "down"
            },
            {
                "number": 8,
                "answer": "CANNING",
                "clue": "A food preservation method using sealed containers.",
                "row": 0,
                "col": 7,
                "direction": "down"
            }
        ]
    },


    # ========================================================
    # BSED - EDUCATION
    # ========================================================

    "BSED": {
        "title": "Education Crossword",

        "words": [
            {
                "number": 1,
                "answer": "EDUCATION",
                "clue": "The process of teaching and learning.",
                "row": 4,
                "col": 0,
                "direction": "across"
            },
            {
                "number": 2,
                "answer": "LEARN",
                "clue": "To gain knowledge or understanding.",
                "row": 3,
                "col": 0,
                "direction": "down"
            },
            {
                "number": 3,
                "answer": "MODULE",
                "clue": "A learning unit containing lessons or activities.",
                "row": 2,
                "col": 1,
                "direction": "down"
            },
            {
                "number": 4,
                "answer": "RUBRIC",
                "clue": "A guide used to evaluate student work.",
                "row": 3,
                "col": 2,
                "direction": "down"
            },
            {
                "number": 5,
                "answer": "TEACHER",
                "clue": "A person who helps students learn.",
                "row": 1,
                "col": 3,
                "direction": "down"
            },
            {
                "number": 6,
                "answer": "CLASS",
                "clue": "A group of students taught together.",
                "row": 2,
                "col": 4,
                "direction": "down"
            },
            {
                "number": 7,
                "answer": "STUDENT",
                "clue": "A person who is learning in an educational setting.",
                "row": 3,
                "col": 5,
                "direction": "down"
            },
            {
                "number": 8,
                "answer": "LESSON",
                "clue": "A planned period of teaching and learning.",
                "row": 0,
                "col": 7,
                "direction": "down"
            }
        ]
    },


    # ========================================================
    # BSBA - BUSINESS ADMINISTRATION
    # ========================================================

    "BSBA": {
        "title": "Business Crossword",

        "words": [
            {
                "number": 1,
                "answer": "MARKETING",
                "clue": "The activity of promoting and delivering value to customers.",
                "row": 5,
                "col": 0,
                "direction": "across"
            },
            {
                "number": 2,
                "answer": "SALES",
                "clue": "The activity of selling products or services.",
                "row": 4,
                "col": 1,
                "direction": "down"
            },
            {
                "number": 3,
                "answer": "PROFIT",
                "clue": "Revenue remaining after costs are deducted.",
                "row": 4,
                "col": 2,
                "direction": "down"
            },
            {
                "number": 4,
                "answer": "MARKET",
                "clue": "A place or system where buyers and sellers interact.",
                "row": 2,
                "col": 3,
                "direction": "down"
            },
            {
                "number": 5,
                "answer": "ASSET",
                "clue": "Something valuable owned by a business.",
                "row": 2,
                "col": 4,
                "direction": "down"
            },
            {
                "number": 6,
                "answer": "BUDGET",
                "clue": "A plan for managing income and expenses.",
                "row": 0,
                "col": 5,
                "direction": "down"
            },
            {
                "number": 7,
                "answer": "BRAND",
                "clue": "A name or symbol that identifies a business or product.",
                "row": 2,
                "col": 7,
                "direction": "down"
            },
            {
                "number": 8,
                "answer": "MANAGER",
                "clue": "A person responsible for directing people or business activities.",
                "row": 1,
                "col": 8,
                "direction": "down"
            }
        ]
    },


    # ========================================================
    # BSFAS - FISHERIES AND AQUATIC SCIENCES
    # ========================================================

    "BSFAS": {
        "title": "Fisheries Crossword",

        "words": [
            {
                "number": 1,
                "answer": "FRESHWATER",
                "clue": "Water with very little dissolved salt, such as in rivers and lakes.",
                "row": 3,
                "col": 0,
                "direction": "across"
            },
            {
                "number": 2,
                "answer": "FISH",
                "clue": "An aquatic animal commonly studied in fisheries.",
                "row": 2,
                "col": 0,
                "direction": "down"
            },
            {
                "number": 3,
                "answer": "FARM",
                "clue": "A place where aquatic organisms may be raised.",
                "row": 1,
                "col": 1,
                "direction": "down"
            },
            {
                "number": 4,
                "answer": "SEA",
                "clue": "A large body of salt water.",
                "row": 2,
                "col": 2,
                "direction": "down"
            },
            {
                "number": 5,
                "answer": "AQUA",
                "clue": "A word associated with water.",
                "row": 0,
                "col": 6,
                "direction": "down"
            },
            {
                "number": 6,
                "answer": "WATER",
                "clue": "The main environment where aquatic organisms live.",
                "row": 0,
                "col": 8,
                "direction": "down"
            },
            {
                "number": 7,
                "answer": "NET",
                "clue": "A tool commonly used for catching fish.",
                "row": 1,
                "col": 7,
                "direction": "down"
            },
            {
                "number": 8,
                "answer": "CRAB",
                "clue": "An aquatic animal with a hard shell and claws.",
                "row": 2,
                "col": 9,
                "direction": "down"
            }
        ]
    }

}

# ============================================================
# REWARDS
# ============================================================



# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    if "user_email" in session:
        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "index.html"
    )


# ============================================================
# REGISTER
# ============================================================
@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        student_id = request.form.get(
            "student_id",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        course = request.form.get(
            "course",
            ""
        ).strip().upper()

        # Check if all fields are complete
        if not name or not student_id or not email or not password or not course:

            flash(
                "Please complete all fields.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        # Check valid course
        if course not in courses:

            flash(
                "Please select a valid course.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        # Check if email already exists in Supabase
        existing_email = (
            supabase
            .table("students")
            .select("id")
            .eq("email", email)
            .limit(1)
            .execute()
        )

        if existing_email.data:

            flash(
                "An account with this email already exists.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        # Check if student ID already exists
        existing_student_id = (
            supabase
            .table("students")
            .select("id")
            .eq("student_id", student_id)
            .limit(1)
            .execute()
        )

        if existing_student_id.data:

            flash(
                "This Student ID is already registered.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        # Hash the password
        hashed_password = generate_password_hash(
            password
        )

        # Save student to Supabase
        supabase.table("students").insert({

            "name": name,

            "student_id": student_id,

            "email": email,

            "password": hashed_password,

            "course": course,

            "points": 0

        }).execute()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html",
        courses=courses
    )

# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        # Find student in Supabase
        response = (
            supabase
            .table("students")
            .select("*")
            .eq("email", email)
            .limit(1)
            .execute()
        )

        student = response.data[0] if response.data else None

        if not student:

            flash(
                "Invalid email or password.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        # Check hashed password
        if not check_password_hash(
            student["password"],
            password
        ):

            flash(
                "Invalid email or password.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        # Save login session
        session["user_email"] = email

        flash(
            "Login successful!",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "login.html"
    )


# ============================================================
# STAFF LOGIN
# ============================================================
@app.route("/staff/login", methods=["GET", "POST"])
def staff_login():

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Find staff account in Supabase
        response = (
            supabase.table("staff_users")
            .select("*")
            .eq("email", email)
            .limit(1)
            .execute()
        )

        staff = response.data[0] if response.data else None

        # Verify account and password
        if not staff or not check_password_hash(
            staff["password_hash"], password
        ):
            flash("Invalid staff email or password.", "error")
            return redirect(url_for("staff_login"))

        # Create a separate staff session
        session.pop("user_email", None)
        session["staff_id"] = staff["id"]
        session["staff_email"] = staff["email"]
        session["staff_name"] = staff["name"]
        session["staff_role"] = staff["role"]

        flash("Staff login successful!", "success")
        return redirect(url_for("staff_dashboard"))

    return render_template("staff_login.html")


# ============================================================
# STAFF DASHBOARD
# ============================================================
@app.route("/staff/dashboard")
def staff_dashboard():

    # Only logged-in staff can access this page
    if "staff_id" not in session:
        flash("Please log in with your staff account.", "error")
        return redirect(url_for("staff_login"))

    return render_template(
        "staff_dashboard.html",
        staff_name=session.get("staff_name", "Staff"),
        staff_role=session.get("staff_role", "staff")
    )

# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    if "user_email" not in session:

        flash(
            "Please login first.",
            "error"
        )

        return redirect(
            url_for("login")
        )

    email = session["user_email"]

    # Get student from Supabase
    response = (
        supabase
        .table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = response.data[0] if response.data else None

    if not student:

        session.clear()

        flash(
            "Your session is no longer valid.",
            "error"
        )

        return redirect(
            url_for("login")
        )

    course_code = student["course"]

    course = courses.get(
        course_code
    )

    if not course:

        flash(
            "Course information not found.",
            "error"
        )

        return redirect(
            url_for("logout")
        )

    return render_template(
        "dashboard.html",
        student=student,
        course=course,
        course_code=course_code
    )




# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# ============================================================
# QUIZ
# ============================================================
@app.route("/quiz", defaults={"game_type": "quiz"})
@app.route("/quiz/<game_type>")
def quiz(game_type):

    if "user_email" not in session:
        return redirect(url_for("login"))

    email = session["user_email"]

    # Get student from Supabase
    response = (
        supabase.table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = response.data[0] if response.data else None

    if not student:
        session.clear()
        flash("Please login again.", "error")
        return redirect(url_for("login"))

    course_code = student["course"]

    if course_code not in quiz_questions:
        flash(
            "Quiz is not available for your course yet.",
            "error"
        )
        return redirect(url_for("dashboard"))

    course = courses[course_code]

    return render_template(
        "quiz_start.html",
        student=student,
        course=course,
        course_code=course_code,
        total_questions=min(
            10,
            len(quiz_questions[course_code])
        )
    )


# ============================================================
# QUIZ START
# ============================================================
@app.route("/quiz/start", methods=["POST"])
def start_quiz():
    if "user_email" not in session:
        return redirect(url_for("login"))

    email = session["user_email"]

    # Get student from Supabase
    response = (
        supabase.table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = response.data[0] if response.data else None

    if not student:
        session.clear()
        flash("Please login again.", "error")
        return redirect(url_for("login"))

    course_code = student["course"]

    if course_code not in quiz_questions:
        flash("Quiz is not available for your course yet.", "error")
        return redirect(url_for("dashboard"))

    # Make a fresh copy of the questions
    questions = [
        {
            "question": item["question"],
            "choices": list(item["choices"]),
            "answer": item["answer"]
        }
        for item in quiz_questions[course_code]
    ]

    # Randomize question order
    random.shuffle(questions)

    # Use up to 10 questions
    questions = questions[:10]

    # Randomize answer choices
    for question in questions:
        random.shuffle(question["choices"])

    session["quiz_questions"] = questions
    session["quiz_index"] = 0
    session["quiz_score"] = 0
    session["quiz_points_awarded"] = False

    return render_template(
        "quiz.html",
        question=questions[0],
        question_number=1,
        total_questions=len(questions),
        course_code=course_code,
        score=0
    )


# ============================================================
# QUIZ ANSWER
# ============================================================

@app.route(
    "/quiz/answer",
    methods=["POST"]
)
def quiz_answer():

    if "user_email" not in session:
        return redirect(url_for("login"))

    email = session["user_email"]

    # Get student from Supabase
    response = (
        supabase
        .table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = response.data[0] if response.data else None

    if not student:
        session.clear()
        return redirect(url_for("login"))

    questions = session.get("quiz_questions", [])
    current_index = session.get("quiz_index", 0)
    score = session.get("quiz_score", 0)

    if not questions:
        return redirect(url_for("quiz"))

    if current_index < 0 or current_index >= len(questions):
        return redirect(url_for("quiz_result"))

    selected_answer = request.form.get(
        "answer", ""
    ).strip()

    current_question = questions[current_index]

    correct_answer = str(
        current_question.get("answer", "")
    ).strip()

    if selected_answer.lower() == correct_answer.lower():
        score += 1

    current_index += 1

    session["quiz_index"] = current_index
    session["quiz_score"] = score

    if current_index >= len(questions):
        return redirect(url_for("quiz_result"))

    next_question = questions[current_index]

    return render_template(
        "quiz.html",
        question=next_question,
        question_number=current_index + 1,
        total_questions=len(questions),
        course_code=student["course"],
        score=score
    )




# ============================================================
# QUIZ RESULT
# ============================================================

@app.route("/quiz/result")
def quiz_result():

    if "user_email" not in session:
        return redirect(url_for("login"))

    score = session.get("quiz_score", 0)
    questions = session.get("quiz_questions", [])
    total = len(questions)

    points_earned = score * 10
    email = session["user_email"]

    # Get student from Supabase
    response = (
        supabase
        .table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = response.data[0] if response.data else None

    if not student:
        session.clear()
        flash("Please login again.", "error")
        return redirect(url_for("login"))

    # Award points only once for this quiz attempt
    if not session.get("quiz_points_awarded", False):

        new_points = student["points"] + points_earned

        supabase.table("students").update({
            "points": new_points
        }).eq("email", email).execute()

        student["points"] = new_points

        session["quiz_points_awarded"] = True

    return render_template(
        "quiz_result.html",
        score=score,
        total=total,
        points_earned=points_earned,
        student=student
    )



# ============================================================
# PUZZLE
# ============================================================
@app.route("/puzzle", defaults={"game_type": "puzzle"})
@app.route("/puzzle/<game_type>")
def puzzle(game_type):

    if "user_email" not in session:
        return redirect(url_for("login"))

    email = session["user_email"]

    # Get student from Supabase
    response = (
        supabase.table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = response.data[0] if response.data else None

    if not student:
        session.clear()
        flash("Please login again.", "error")
        return redirect(url_for("login"))

    course_code = student["course"]

    if course_code not in puzzle_questions:
        flash(
            "Puzzle is not available for your course yet.",
            "error"
        )
        return redirect(url_for("dashboard"))

    course = courses[course_code]

    return render_template(
        "puzzle_start.html",
        student=student,
        course=course,
        course_code=course_code,
        total_questions=len(
            puzzle_questions[course_code]
        )
    )

# ============================================================
# PUZZLE START
# ============================================================
@app.route("/puzzle/start", methods=["POST"])
def start_puzzle():

    if "user_email" not in session:
        return redirect(url_for("login"))

    email = session["user_email"]

    response = (
        supabase.table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = response.data[0] if response.data else None

    if not student:
        session.clear()
        flash("Please login again.", "error")
        return redirect(url_for("login"))

    course_code = student["course"]

    if course_code not in puzzle_questions:
        flash(
            "Puzzle is not available for your course yet.",
            "error"
        )
        return redirect(url_for("dashboard"))

    questions = puzzle_questions[course_code]

    session["puzzle_questions"] = questions
    session["puzzle_index"] = 0
    session["puzzle_score"] = 0
    session["puzzle_points_awarded"] = False

    return render_template(
        "puzzle.html",
        question=questions[0],
        question_number=1,
        total_questions=len(questions),
        course_code=course_code,
        score=0
    )

# ============================================================
# PUZZLE ANSWER
# ============================================================

# ============================================================
# PUZZLE ANSWER
# ============================================================
@app.route("/puzzle/answer", methods=["POST"])
def puzzle_answer():

    if "user_email" not in session:
        return redirect(url_for("login"))

    email = session["user_email"]

    response = (
        supabase.table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = response.data[0] if response.data else None

    if not student:
        session.clear()
        flash("Please login again.", "error")
        return redirect(url_for("login"))

    questions = session.get("puzzle_questions", [])
    current_index = session.get("puzzle_index", 0)
    score = session.get("puzzle_score", 0)

    if not questions:
        flash("No puzzle questions found.", "error")
        return redirect(url_for("puzzle"))

    if current_index < 0 or current_index >= len(questions):
        return redirect(url_for("puzzle_result"))

    current_question = questions[current_index]

    correct_answer = str(
        current_question.get("answer", "")
    ).strip()

    selected_answer = request.form.get(
        "answer", ""
    ).strip()

    normalized_correct = "".join(
        character
        for character in correct_answer.upper()
        if character.isalnum()
    )

    normalized_selected = "".join(
        character
        for character in selected_answer.upper()
        if character.isalnum()
    )

    if normalized_selected == normalized_correct:
        score += 1

    current_index += 1

    session["puzzle_score"] = score
    session["puzzle_index"] = current_index

    if current_index >= len(questions):
        return redirect(url_for("puzzle_result"))

    next_question = questions[current_index]

    return render_template(
        "puzzle.html",
        question=next_question,
        question_number=current_index + 1,
        total_questions=len(questions),
        course_code=student["course"],
        score=score
    )


# ============================================================
# PUZZLE RESULT
# ============================================================
@app.route("/puzzle/result")
def puzzle_result():

    if "user_email" not in session:
        return redirect(url_for("login"))

    email = session["user_email"]

    # Get student from Supabase
    response = (
        supabase.table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = response.data[0] if response.data else None

    if not student:
        session.clear()
        flash("Please login again.", "error")
        return redirect(url_for("login"))

    # Get puzzle results
    score = session.get("puzzle_score", 0)
    questions = session.get("puzzle_questions", [])
    total = len(questions)

    # 10 points per correct answer
    points_earned = score * 10

    # Add points only once per attempt
    if not session.get("puzzle_points_awarded", False):

        new_points = student["points"] + points_earned

        supabase.table("students").update({
            "points": new_points
        }).eq("id", student["id"]).execute()

        student["points"] = new_points
        session["puzzle_points_awarded"] = True

    return render_template(
        "puzzle_result.html",
        score=score,
        total=total,
        points_earned=points_earned,
        student=student
    )


# ============================================================
# CROSSWORD START
# ============================================================
@app.route("/crossword", defaults={"game_type": "crossword"})
@app.route("/crossword/<game_type>")
def crossword(game_type):

    if "user_email" not in session:
        return redirect(url_for("login"))

    email = session["user_email"]

    # Get student from Supabase
    response = (
        supabase.table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = response.data[0] if response.data else None

    if not student:
        session.clear()
        flash("Please login again.", "error")
        return redirect(url_for("login"))

    course_code = student["course"]

    if course_code not in crossword_questions:
        flash(
            "Crossword is not available for your course yet.",
            "error"
        )
        return redirect(url_for("dashboard"))

    course = courses[course_code]

    crossword_data = crossword_questions[course_code]

    return render_template(
        "crossword_start.html",
        student=student,
        course=course,
        course_code=course_code,
        crossword=crossword_data
    )


# ============================================================
# START CROSSWORD GAME
# ============================================================
@app.route("/crossword/start", methods=["POST"])
def start_crossword():

    if "user_email" not in session:
        return redirect(url_for("login"))

    email = session["user_email"]

    # Get student from Supabase
    response = (
        supabase.table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = response.data[0] if response.data else None

    if not student:
        session.clear()
        flash("Please login again.", "error")
        return redirect(url_for("login"))

    course_code = student["course"]

    if course_code not in crossword_questions:
        flash("Crossword is not available for your course yet.", "error")
        return redirect(url_for("dashboard"))

    course = courses[course_code]
    crossword_data = crossword_questions[course_code]

    # Reset the points-awarded flag for this new attempt
    session["crossword_points_awarded"] = False

    return render_template(
        "crossword.html",
        student=student,
        course=course,
        course_code=course_code,
        crossword=crossword_data
    )

# ============================================================
# CROSSWORD ANSWER
# ============================================================
@app.route("/crossword/answer", methods=["POST"])
def crossword_answer():

    if "user_email" not in session:
        return redirect(url_for("login"))

    email = session["user_email"]

    # Get student from Supabase
    response = (
        supabase.table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = response.data[0] if response.data else None

    if not student:
        session.clear()
        flash("Please login again.", "error")
        return redirect(url_for("login"))

    course_code = student["course"]

    if course_code not in crossword_questions:
        flash(
            "Crossword is not available for your course yet.",
            "error"
        )
        return redirect(url_for("dashboard"))

    crossword_data = crossword_questions[course_code]
    words = crossword_data["words"]

    correct_count = 0
    total_words = len(words)
    results = []

    for word in words:
        field_name = f"word_{word['number']}"

        submitted_answer = request.form.get(
            field_name, ""
        ).strip().upper()

        correct_answer = word["answer"].strip().upper()

        is_correct = submitted_answer == correct_answer

        if is_correct:
            correct_count += 1

        results.append({
            "number": word["number"],
            "clue": word["clue"],
            "submitted_answer": submitted_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

    # 5 points per correct answer
    points_earned = correct_count * 5

    # Save points to Supabase only once per session attempt
    if not session.get("crossword_points_awarded", False):

        new_points = student["points"] + points_earned

        supabase.table("students").update({
            "points": new_points
        }).eq("id", student["id"]).execute()

        student["points"] = new_points
        session["crossword_points_awarded"] = True

    return render_template(
        "crossword_result.html",
        crossword=crossword_data,
        results=results,
        correct_count=correct_count,
        total_words=total_words,
        points_earned=points_earned,
        student=student,
        course_code=course_code
    )
# ============================================================
# REDEEM REWARD
# ============================================================

@app.route("/redeem/<reward_name>", methods=["POST"])
def redeem_reward(reward_name):

    if "user_email" not in session:
        return redirect(url_for("login"))

    email = session["user_email"]

    # Get student from Supabase
    student_response = (
        supabase.table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = student_response.data[0] if student_response.data else None

    if not student:
        session.clear()
        flash("Please login again.", "error")
        return redirect(url_for("login"))

    # Convert URL slug to reward name
    reward_slug = reward_name.replace("-", " ").strip()

    # Search for reward without case sensitivity
    reward_response = (
        supabase.table("rewards")
        .select("*")
        .ilike("name", reward_slug)
        .limit(1)
        .execute()
    )

    reward = reward_response.data[0] if reward_response.data else None

    if not reward:
        flash(
            f"Reward not found in Supabase. Searched for: {reward_slug}",
            "error"
        )
        return redirect(url_for("dashboard"))

    # Check required points and stock
    required_points = reward["points_required"]

    if reward["stock"] <= 0:
        flash("This reward is out of stock.", "error")
        return redirect(url_for("dashboard"))

    if student["points"] < required_points:
        flash("You don't have enough points for this reward.", "error")
        return redirect(url_for("dashboard"))

    # Generate redemption code
    redemption_code = str(uuid.uuid4()).replace("-", "").upper()[:8]

    # Deduct points
    new_points = student["points"] - required_points

    supabase.table("students").update({
        "points": new_points
    }).eq("id", student["id"]).execute()

    # Reduce reward stock
    supabase.table("rewards").update({
        "stock": reward["stock"] - 1
    }).eq("id", reward["id"]).execute()

    # Create redemption record
    supabase.table("redemptions").insert({
        "student_id": student["id"],
        "reward_id": reward["id"],
        "redemption_code": redemption_code,
        "qr_data": redemption_code,
        "status": "pending"
    }).execute()

    session["redeemed_reward"] = {
        "name": reward["name"],
        "points": required_points,
        "code": redemption_code
    }

    return redirect(url_for("redemption_success"))


# ============================================================
# REDEMPTION SUCCESS
# ============================================================
@app.route("/redemption-success")
def redemption_success():

    if "user_email" not in session:
        return redirect(url_for("login"))

    reward = session.get("redeemed_reward")

    if not reward:
        return redirect(url_for("dashboard"))

    email = session["user_email"]

    # Get student from Supabase
    response = (
        supabase
        .table("students")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    student = response.data[0] if response.data else None

    if not student:
        session.clear()
        return redirect(url_for("login"))

    return render_template(
        "redemption_success.html",
        reward=reward,
        student=student
    )

# ============================================================
# CLAIMING STATION
#
@app.route("/claim", methods=["GET", "POST"])
def claim_reward():

    # Block access unless staff is logged in
    if "staff_id" not in session:
        return redirect(url_for("staff_login"))

    result = None

    # Keep the rest of your existing claim_reward() code here

    # Keep the rest of your existing claim_reward() code below

    if request.method == "POST":

        code = request.form.get(
            "code",
            ""
        ).strip().upper()

        # Find redemption in Supabase
        response = (
            supabase
            .table("redemptions")
            .select(
                "id, redemption_code, status, claimed_at, "
                "students(name, student_id), rewards(name)"
            )
            .eq("redemption_code", code)
            .limit(1)
            .execute()
        )

        redemption = (
            response.data[0]
            if response.data
            else None
        )

        if not redemption:

            result = {
                "success": False,
                "message": "Invalid redemption code."
            }

        elif redemption["status"] == "claimed":

            result = {
                "success": False,
                "message": "This reward has already been claimed."
            }

        elif redemption["status"] != "pending":

            result = {
                "success": False,
                "message": "This redemption is not available for claiming."
            }

        else:

            # Mark the redemption as claimed
            update_response = (
                supabase
                .table("redemptions")
                .update({
                    "status": "claimed",
                    "claimed_at": datetime.now(timezone.utc).isoformat()
                })
                .eq("id", redemption["id"])
                .eq("status", "pending")
                .execute()
            )

            if not update_response.data:

                result = {
                    "success": False,
                    "message": "This reward may already have been claimed. Please verify the code again."
                }

            else:

                student = redemption.get("students") or {}
                reward = redemption.get("rewards") or {}

                result = {
                    "success": True,
                    "student_name": student.get("name", "Unknown"),
                    "student_id": student.get("student_id", "Unknown"),
                    "reward_name": reward.get("name", "Unknown"),
                    "message": "Reward verified successfully!"
                }

    return render_template(
        "claim.html",
        result=result
    )




# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
"""
Pre-cached sample analyses for 3 curated fitness YouTube videos.
Used for:
1. One-click "Try Example" feature in frontend for instant judge evaluation.
2. Foolproof fallback if Gemini quota is exceeded or video embedding is restricted.
3. Fast offline development and testing.
"""

SAMPLE_VIDEOS = {
    "sample1": {
        "id": "sample1",
        "title": "5 Essential Dumbbell Exercises for Beginners | Full Body Routine",
        "youtube_url": "https://www.youtube.com/watch?v=U0bhE67HuDY",
        "duration": 620,
        "category": "Beginner Dumbbell",
        "analysis": {
            "summary": "A foundational full-body dumbbell workout designed for beginners, introducing 5 compound movements with progressive form cues and tempo instructions.",
            "moments": [
                {
                    "timestamp_seconds": 15,
                    "title": "Workout Overview & Equipment Needs",
                    "description": "Coach introduces the 5 dumbbell movements and explains how to select the right starting weight."
                },
                {
                    "timestamp_seconds": 75,
                    "title": "Exercise 1: Goblet Squat Setup",
                    "description": "Demonstrates vertical torso posture, foot stance, and holding dumbbell at chest height."
                },
                {
                    "timestamp_seconds": 180,
                    "title": "Exercise 2: Dumbbell Romanian Deadlift",
                    "description": "Explains the hip-hinge mechanic versus knee flexion, emphasizing flat back and glute engagement."
                },
                {
                    "timestamp_seconds": 295,
                    "title": "Exercise 3: Flat Bench Dumbbell Press",
                    "description": "Breaks down 45-degree elbow tuck and shoulder retraction to protect the rotator cuff."
                },
                {
                    "timestamp_seconds": 410,
                    "title": "Exercise 4: Supported Single-Arm Row",
                    "description": "Covers bench bracing, pulling towards hip rather than chest to maximize lat activation."
                },
                {
                    "timestamp_seconds": 515,
                    "title": "Exercise 5: Standing Overhead Press",
                    "description": "Teaches glute and core bracing to avoid hyperextending lumbar spine during overhead pressing."
                },
                {
                    "timestamp_seconds": 590,
                    "title": "Cool Down & Progression Advice",
                    "description": "Recaps weekly progression rules and rest periods for sustainable strength gains."
                }
            ],
            "hook_score": 8.2,
            "hook_dimensions": [
                {
                    "name": "Clarity",
                    "score": 9,
                    "timestamp_seconds": 6,
                    "observation": "Title and direct verbal statement of the 5-exercise goal occur within the first 6 seconds.",
                    "suggestion": "Keep the on-screen bullet points visible for 2 seconds longer for visual learners."
                },
                {
                    "name": "Curiosity",
                    "score": 7,
                    "timestamp_seconds": 14,
                    "observation": "Mentions 'the #1 mistake beginners make with dumbbells', creating intrigue before the workout begins.",
                    "suggestion": "Tease which specific exercise this mistake belongs to so viewers stay engaged until that timestamp."
                },
                {
                    "name": "Pacing",
                    "score": 8,
                    "timestamp_seconds": 22,
                    "observation": "Minimal fluff and fast transition from intro directly into the warm-up recommendations.",
                    "suggestion": "Slightly tighten the equipment disclaimer to save 4 seconds."
                },
                {
                    "name": "Payoff Promise",
                    "score": 9,
                    "timestamp_seconds": 18,
                    "observation": "Guarantees a complete full-body routine doable in 30 minutes with a single pair of dumbbells.",
                    "suggestion": "Reiterate this promise visually with an on-screen workout summary graphic."
                }
            ],
            "current_title_assessment": "Clear and searchable with good SEO, but slightly generic and does not convey the time efficiency or pain-free focus.",
            "title_alternatives": [
                {
                    "title": "Build Full-Body Strength With Just 2 Dumbbells (Beginner Routine)",
                    "strengths": "Directly targets the minimal equipment benefit and uses empowering strength-focused phrasing.",
                    "weaknesses": "Omits the specific number 5 which some list-seekers prefer.",
                    "rubric_score": 9
                },
                {
                    "title": "The Only 5 Dumbbell Exercises You Need as a Beginner (Full Body)",
                    "strengths": "Strong curiosity hook ('The Only 5') without crossing into deceptive clickbait.",
                    "weaknesses": "Could sound slightly dogmatic to experienced lifters.",
                    "rubric_score": 9
                },
                {
                    "title": "Start Here: 20-Minute Dumbbell Workout for Total Beginners",
                    "strengths": "Low barrier to entry with 'Start Here' directive and concrete time commitment.",
                    "weaknesses": "Focuses more on time than exercise mastery.",
                    "rubric_score": 8
                }
            ],
            "recommended_title_index": 1,
            "readiness_score": 86,
            "score_factors": [
                {
                    "name": "Hook Strength",
                    "score": 21,
                    "evidence": "Engaging 30-second opening clearly outlines workout purpose with zero dead time."
                },
                {
                    "name": "Content Structure",
                    "score": 23,
                    "evidence": "Logical progression from lower to upper body compound lifts with distinct chapter markers."
                },
                {
                    "name": "Pacing",
                    "score": 21,
                    "evidence": "Explanations are concise, showing side and front angles during repetitions."
                },
                {
                    "name": "Title Fit",
                    "score": 21,
                    "evidence": "Direct match between title premise and demonstrated workout routine."
                }
            ],
            "top_improvements": [
                "Add an on-screen timer during demonstrations to reinforce suggested rep tempo (e.g., 3-1-1).",
                "Display common form errors side-by-side with correct form using a red/green split screen.",
                "Include equipment-free warm-up movements before jumping into weighted goblet squats."
            ]
        },
        "panel": {
            "panel_reactions": [
                {
                    "persona": "Gym Beginner",
                    "overall_rating": "Welcoming, Confidence-Building, and Safe",
                    "highlights": [
                        {
                            "timestamp_seconds": 80,
                            "reaction": "Holding the dumbbell like a goblet made balance feel intuitive and safe.",
                            "sentiment": "positive",
                            "suggestion": None
                        },
                        {
                            "timestamp_seconds": 190,
                            "reaction": "The cue 'imagine closing a car door with your hips' clarified Romanian deadlifts immediately.",
                            "sentiment": "positive",
                            "suggestion": None
                        }
                    ],
                    "concerns": [
                        {
                            "timestamp_seconds": 305,
                            "reaction": "I don't own a weight bench, so the flat bench press felt inaccessible.",
                            "sentiment": "negative",
                            "suggestion": "Demonstrate the floor press as an alternative for home users without a bench."
                        }
                    ]
                },
                {
                    "persona": "Experienced Lifter",
                    "overall_rating": "Solid Fundamentals, but Too Introductory for Strength Progressions",
                    "highlights": [
                        {
                            "timestamp_seconds": 300,
                            "reaction": "The 45-degree elbow path coaching on the press is biomechanically sound and shoulder-safe.",
                            "sentiment": "positive",
                            "suggestion": None
                        }
                    ],
                    "concerns": [
                        {
                            "timestamp_seconds": 420,
                            "reaction": "No mention of rep-in-reserve (RIR) or progressive overload principles.",
                            "sentiment": "negative",
                            "suggestion": "Add a quick 10-second tip on when to increase dumbbell weight."
                        }
                    ]
                },
                {
                    "persona": "Home Workout Viewer",
                    "overall_rating": "Mostly Feasible, but Needs Floor Substitutions",
                    "highlights": [
                        {
                            "timestamp_seconds": 25,
                            "reaction": "Appreciated that only one pair of dumbbells is required for all five exercises.",
                            "sentiment": "positive",
                            "suggestion": None
                        }
                    ],
                    "concerns": [
                        {
                            "timestamp_seconds": 415,
                            "reaction": "The single-arm row relies on bracing against a gym bench.",
                            "sentiment": "negative",
                            "suggestion": "Show how to brace against a sturdy dining chair or sofa."
                        }
                    ]
                }
            ],
            "disagreements": [
                {
                    "timestamp_seconds": 305,
                    "topic": "Bench Press vs Floor Press",
                    "beginner": "Happy with the clear visual form, but puzzled about how to set it up without a gym bench.",
                    "experienced": "Prefers standard bench for full range of motion at the bottom of the press.",
                    "home_viewer": "Needs a floor press demonstration; bench requirement breaks the home workout promise."
                },
                {
                    "timestamp_seconds": 185,
                    "topic": "Hinge Movement Depth and Tempo",
                    "beginner": "Appreciates the cautious pace and emphasis on avoiding lower back strain.",
                    "experienced": "Finds the explanation overly slow and would prefer cueing hamstring tension over repeated setup angles.",
                    "home_viewer": "Likes the slow pace because apartment mirrors are limited and self-checking takes time."
                }
            ]
        },
        "shorts": [
            {
                "start_seconds": 75,
                "end_seconds": 118,
                "duration_seconds": 43,
                "title": "Master the Dumbbell Goblet Squat in 40 Seconds",
                "hook_caption": "Stop squatting like this! Hold the dumbbell here instead 👇",
                "reason_standalone": "Shows the exact vertical torso cue and dumbbell grip to fix common squat back pain immediately."
            },
            {
                "start_seconds": 180,
                "end_seconds": 222,
                "duration_seconds": 42,
                "title": "The Car Door Trick for Romanian Deadlifts",
                "hook_caption": "The #1 cue for pain-free Romanian Deadlifts 🚪",
                "reason_standalone": "Uses the intuitive 'closing the car door with hips' analogy that instantly clicks for viewers."
            }
        ]
    },
    "sample2": {
        "id": "sample2",
        "title": "How To Squat With Proper Form (Step-By-Step Checklist)",
        "youtube_url": "https://www.youtube.com/watch?v=bEv6CCg2BC8",
        "duration": 540,
        "category": "Strength / Barbell",
        "analysis": {
            "summary": "An in-depth technical biomechanics guide breaking down the barbell back squat into setup, descent, depth criteria, and ascent cues.",
            "moments": [
                {
                    "timestamp_seconds": 10,
                    "title": "The 4-Step Squat Framework",
                    "description": "Introduces rack height, walkout, foot angle, and bracing sequence."
                },
                {
                    "timestamp_seconds": 65,
                    "title": "Bar Placement & Shelf Creation",
                    "description": "Compares high-bar versus low-bar placement on upper trapezius and rear deltoids."
                },
                {
                    "timestamp_seconds": 150,
                    "title": "The 3-Step Walkout Rule",
                    "description": "Demonstrates efficient walkout mechanics to conserve energy under heavy loads."
                },
                {
                    "timestamp_seconds": 240,
                    "title": "Breathing & Intra-Abdominal Pressure",
                    "description": "Deep dive into the Valsalva maneuver and 360-degree core expansion."
                },
                {
                    "timestamp_seconds": 330,
                    "title": "Depth: Parallel vs Below Parallel",
                    "description": "Visualizing hip crease relative to knee joint and addressing butt wink."
                },
                {
                    "timestamp_seconds": 420,
                    "title": "Common Error: Knee Cave (Valgus Collapse)",
                    "description": "Analyzing hip abductor weakness versus stance width and ankle mobility."
                },
                {
                    "timestamp_seconds": 510,
                    "title": "Troubleshooting Checklist Summary",
                    "description": "Summary checklist graphics for lifters to screenshot and take to the gym."
                }
            ],
            "hook_score": 8.7,
            "hook_dimensions": [
                {
                    "name": "Clarity",
                    "score": 9,
                    "timestamp_seconds": 5,
                    "observation": "Clear hook stating 'Stop guessing your squat depth—here is the exact 4-step checklist'.",
                    "suggestion": "State whether high-bar or low-bar will be the primary focus."
                },
                {
                    "name": "Curiosity",
                    "score": 8,
                    "timestamp_seconds": 12,
                    "observation": "Shows a split-screen comparison of a painful knee-dive squat against a clean, balanced rep.",
                    "suggestion": "Ask the viewer directly: 'Which of these two walkouts do you do?'"
                },
                {
                    "name": "Pacing",
                    "score": 9,
                    "timestamp_seconds": 20,
                    "observation": "Fast visual cuts between anatomical diagrams and barbell demonstration.",
                    "suggestion": "Maintain this brisk pace into the breathing section."
                },
                {
                    "name": "Payoff Promise",
                    "score": 9,
                    "timestamp_seconds": 25,
                    "observation": "Promises immediate relief from lower back and knee discomfort after applying checklist.",
                    "suggestion": "Strong and credible promise grounded in biomechanical alignment."
                }
            ],
            "current_title_assessment": "Solid instructional title, but could highlight the injury-prevention and immediate fix angle more powerfully.",
            "title_alternatives": [
                {
                    "title": "Fix Your Squat Form in 4 Steps (Stop Knee & Back Pain)",
                    "strengths": "Directly targets high-intent pain points (knee and back pain) while promising a simple 4-step framework.",
                    "weaknesses": "Sounds like an injury rehab video rather than general strength optimization.",
                    "rubric_score": 9
                },
                {
                    "title": "The Step-By-Step Squat Checklist Every Lifter Needs",
                    "strengths": "Authoritative tone that appeals to both beginners and intermediate trainees.",
                    "weaknesses": "Slightly less urgent than pain-reduction phrasing.",
                    "rubric_score": 9
                },
                {
                    "title": "Are You Squatting Wrong? Master Perfect Depth & Walkout",
                    "strengths": "Curiosity-driven question hook focusing on the two most visible technical errors.",
                    "weaknesses": "Negative question framing can trigger defensiveness.",
                    "rubric_score": 8
                }
            ],
            "recommended_title_index": 0,
            "readiness_score": 91,
            "score_factors": [
                {
                    "name": "Hook Strength",
                    "score": 23,
                    "evidence": "High-clarity split screen and pain-point identification in first 15 seconds."
                },
                {
                    "name": "Content Structure",
                    "score": 24,
                    "evidence": "Chronological progression matching the physical execution of a squat rep."
                },
                {
                    "name": "Pacing",
                    "score": 22,
                    "evidence": "Excellent anatomical overlays keep technical explanations visually dynamic."
                },
                {
                    "name": "Title Fit",
                    "score": 22,
                    "evidence": "Checklist promised in title is delivered with screenshot-ready summaries."
                }
            ],
            "top_improvements": [
                "Provide alternative mobility drills for lifters with limited ankle dorsiflexion.",
                "Clarify footwear recommendations (flat shoes/barefoot vs Olympic lifting shoes with raised heel).",
                "Add audio cue sound effects when demonstrating the Valsalva brace."
            ]
        },
        "panel": {
            "panel_reactions": [
                {
                    "persona": "Gym Beginner",
                    "overall_rating": "Informative but Intimidating Without Machine Alternatives",
                    "highlights": [
                        {
                            "timestamp_seconds": 155,
                            "reaction": "The 3-step walkout rule made approaching the squat rack feel systematic and less scary.",
                            "sentiment": "positive",
                            "suggestion": None
                        }
                    ],
                    "concerns": [
                        {
                            "timestamp_seconds": 70,
                            "reaction": "Unsure how to find my 'rear deltoid shelf' without someone in person to touch my shoulders.",
                            "sentiment": "negative",
                            "suggestion": "Suggest practicing bar placement with a broomstick at home first."
                        },
                        {
                            "timestamp_seconds": 245,
                            "reaction": "The Valsalva maneuver explanation sounded scary regarding blood pressure.",
                            "sentiment": "negative",
                            "suggestion": "Reassure beginners that normal controlled breathing is fine for lighter weights."
                        }
                    ]
                },
                {
                    "persona": "Experienced Lifter",
                    "overall_rating": "Exceptional Technical Breakdown and Visual Cueing",
                    "highlights": [
                        {
                            "timestamp_seconds": 160,
                            "reaction": "Emphasis on the 3-step walkout is golden—too many lifters waste energy taking 6 steps back.",
                            "sentiment": "positive",
                            "suggestion": None
                        },
                        {
                            "timestamp_seconds": 340,
                            "reaction": "Distinguishing between anatomical hip anatomy and true mobility restrictions was refreshing.",
                            "sentiment": "positive",
                            "suggestion": None
                        }
                    ],
                    "concerns": [
                        {
                            "timestamp_seconds": 435,
                            "reaction": "Would like more discussion on adductor magnus recruitment in wide vs moderate stance.",
                            "sentiment": "neutral",
                            "suggestion": "Brief mention of stance width variation according to femur-to-torso ratio."
                        }
                    ]
                },
                {
                    "persona": "Home Workout Viewer",
                    "overall_rating": "Limited Direct Applicability Without a Heavy Barbell Rack",
                    "highlights": [
                        {
                            "timestamp_seconds": 335,
                            "reaction": "The hip-crease depth visual applies equally well to bodyweight and goblet squats.",
                            "sentiment": "positive",
                            "suggestion": None
                        }
                    ],
                    "concerns": [
                        {
                            "timestamp_seconds": 15,
                            "reaction": "Entire video requires a commercial power rack, Olympic barbell, and bumper plates.",
                            "sentiment": "negative",
                            "suggestion": "Include a 30-second callout for adapting these cues to goblet or backpack squats."
                        }
                    ]
                }
            ],
            "disagreements": [
                {
                    "timestamp_seconds": 240,
                    "topic": "Valsalva Maneuver vs Continuous Breathing",
                    "beginner": "Intimidated by holding breath and fears dizziness under load.",
                    "experienced": "Insists Valsalva is mandatory for spinal stiffness and high loads.",
                    "home_viewer": "Prefers continuous breathing since home workouts rarely involve 1RM maximal strain."
                },
                {
                    "timestamp_seconds": 330,
                    "topic": "Depth Standard (Parallel vs Ass-to-Grass)",
                    "beginner": "Worried deep squats will ruin knees; wants permission to stop above parallel.",
                    "experienced": "Demands crease-below-patella depth for full quadriceps and glute hypertrophy.",
                    "home_viewer": "Focuses on whatever depth can be maintained pain-free in a narrow living room space."
                }
            ]
        },
        "shorts": [
            {
                "start_seconds": 150,
                "end_seconds": 195,
                "duration_seconds": 45,
                "title": "Stop Wasting Energy: The 3-Step Squat Walkout Rule",
                "hook_caption": "Are you taking 6 steps back from the rack? Stop right now! 🛑",
                "reason_standalone": "Provides a crisp, standalone mechanical breakdown of the optimal 3-step walkout under heavy load."
            },
            {
                "start_seconds": 330,
                "end_seconds": 372,
                "duration_seconds": 42,
                "title": "How Deep Should You Actually Squat? (Hip Crease Guide)",
                "hook_caption": "Are your squats deep enough? Check this one line 📏",
                "reason_standalone": "Clear visual comparison showing hip crease vs knee joint line for valid, safe squat depth."
            }
        ]
    },
    "sample3": {
        "id": "sample3",
        "title": "20-Minute No Equipment Full Body HIIT (Apartment Friendly / Low Impact)",
        "youtube_url": "https://www.youtube.com/watch?v=cbKkB3POqaY",
        "duration": 1200,
        "category": "Home / Calisthenics",
        "analysis": {
            "summary": "A zero-equipment, joint-friendly high-intensity interval workout specifically structured for quiet apartment living without jumping.",
            "moments": [
                {
                    "timestamp_seconds": 10,
                    "title": "Apartment Friendly Guidelines",
                    "description": "Coach explains no-jumping modifications to keep noise zero for downstairs neighbors."
                },
                {
                    "timestamp_seconds": 80,
                    "title": "Dynamic Warm-Up: Arm Circles & Torso Twists",
                    "description": "Prepares joint synovial fluid and elevates heart rate progressively."
                },
                {
                    "timestamp_seconds": 210,
                    "title": "Circuit 1: Squat to Calf Raise",
                    "description": "Low-impact power substitution replacing jump squats with explosive triple extension."
                },
                {
                    "timestamp_seconds": 390,
                    "title": "Circuit 1: Incline Plank Taps",
                    "description": "Demonstrates anti-rotational core stabilization with optional knee-down variation."
                },
                {
                    "timestamp_seconds": 570,
                    "title": "Circuit 2: Reverse Lunge with Knee Drive",
                    "description": "Unilateral leg stability work avoiding high-impact landing stress on knee joints."
                },
                {
                    "timestamp_seconds": 750,
                    "title": "Circuit 2: Standing Cross-Body Punches",
                    "description": "Rotational cardio segment elevating metabolic rate without foot stomping."
                },
                {
                    "timestamp_seconds": 960,
                    "title": "Finisher: Slow Eccentric Push-Ups / Pike Hold",
                    "description": "Upper body burnout with 3-second descent to stimulate muscle tension."
                },
                {
                    "timestamp_seconds": 1140,
                    "title": "Deep Breathing & Hamstring Decompression",
                    "description": "Parasympathetic cool down bringing heart rate back to baseline."
                }
            ],
            "hook_score": 9.1,
            "hook_dimensions": [
                {
                    "name": "Clarity",
                    "score": 10,
                    "timestamp_seconds": 4,
                    "observation": "States 'Zero jumping, zero equipment, 100% neighbor-friendly' in the first 4 seconds.",
                    "suggestion": "Excellent clarity; keep this concise formula."
                },
                {
                    "name": "Curiosity",
                    "score": 8,
                    "timestamp_seconds": 12,
                    "observation": "Shows heart-rate monitor telemetry proving low-impact can match high-impact calorie burn.",
                    "suggestion": "Show the monitor spike visually as a teaser for circuit intensity."
                },
                {
                    "name": "Pacing",
                    "score": 9,
                    "timestamp_seconds": 18,
                    "observation": "Immediately starts synchronized warm-up while talking; no lengthy sit-down monologue.",
                    "suggestion": "Keep background music volume balanced so verbal breathing cues stay audible."
                },
                {
                    "name": "Payoff Promise",
                    "score": 9,
                    "timestamp_seconds": 22,
                    "observation": "Promises an intense sweat session with zero joint aches and zero neighbor complaints.",
                    "suggestion": "Include an on-screen interval countdown graphic (40s work / 20s rest)."
                }
            ],
            "current_title_assessment": "Very descriptive and keyword-rich, effectively hitting both 'No Equipment' and 'Apartment Friendly'.",
            "title_alternatives": [
                {
                    "title": "20-Min Quiet HIIT Workout (Burn Fat With ZERO Jumping)",
                    "strengths": "Strong emotional hook for apartment dwellers who feel guilty making floor noise.",
                    "weaknesses": "Slightly sensationalist 'Burn Fat' trope.",
                    "rubric_score": 9
                },
                {
                    "title": "Low Impact, High Sweat: 20-Min Full Body Home Workout",
                    "strengths": "Clever rhyme ('Low Impact, High Sweat') that highlights the core contrast.",
                    "weaknesses": "Less searchable than explicit keyword 'Apartment Friendly'.",
                    "rubric_score": 9
                },
                {
                    "title": "No Equipment, No Noise: The Ultimate Apartment Cardio Routine",
                    "strengths": "Positions the video as the definitive solution for apartment cardio.",
                    "weaknesses": "Omits specific time duration.",
                    "rubric_score": 8
                }
            ],
            "recommended_title_index": 0,
            "readiness_score": 93,
            "score_factors": [
                {
                    "name": "Hook Strength",
                    "score": 24,
                    "evidence": "Immediate problem-solution hook addressing apartment living constraints."
                },
                {
                    "name": "Content Structure",
                    "score": 24,
                    "evidence": "Follow-along intervals with visible timer, rest countdowns, and form cues."
                },
                {
                    "name": "Pacing",
                    "score": 23,
                    "evidence": "Consistent energy and seamless transitions between intervals."
                },
                {
                    "name": "Title Fit",
                    "score": 22,
                    "evidence": "Every movement strictly fulfills the low-impact and apartment-friendly promise."
                }
            ],
            "top_improvements": [
                "Add an in-picture mini preview box showing the upcoming exercise 5 seconds before each rest ends.",
                "Display a sound decibel meter graphic as a fun gamification proof that reps are whisper-quiet.",
                "Provide a wrist-friendly push-up modification (on fists or elevated surface) for sensitive joints."
            ]
        },
        "panel": {
            "panel_reactions": [
                {
                    "persona": "Gym Beginner",
                    "overall_rating": "Extremely Doable and Free of Joint Pain",
                    "highlights": [
                        {
                            "timestamp_seconds": 220,
                            "reaction": "Replacing jump squats with calf raises kept my knees from aching while still raising heart rate.",
                            "sentiment": "positive",
                            "suggestion": None
                        },
                        {
                            "timestamp_seconds": 400,
                            "reaction": "Incline plank tap option on knees allowed me to finish the whole set without dropping.",
                            "sentiment": "positive",
                            "suggestion": None
                        }
                    ],
                    "concerns": [
                        {
                            "timestamp_seconds": 970,
                            "reaction": "Slow eccentric push-ups were still too hard for my upper body strength.",
                            "sentiment": "negative",
                            "suggestion": "Show a wall push-up variation alongside the floor demonstration."
                        }
                    ]
                },
                {
                    "persona": "Experienced Lifter",
                    "overall_rating": "Great Conditioning Conditioning Work, But Not for Hypertrophy",
                    "highlights": [
                        {
                            "timestamp_seconds": 975,
                            "reaction": "The 3-second eccentric tempo on push-ups effectively created mechanical tension without weights.",
                            "sentiment": "positive",
                            "suggestion": None
                        }
                    ],
                    "concerns": [
                        {
                            "timestamp_seconds": 760,
                            "reaction": "Standing shadow boxing feels like low resistance busywork rather than targeted strength.",
                            "sentiment": "negative",
                            "suggestion": "Suggest holding small water bottles or resistance bands to increase resistance."
                        }
                    ]
                },
                {
                    "persona": "Home Workout Viewer",
                    "overall_rating": "The Holy Grail for Small Apartment Dwellers",
                    "highlights": [
                        {
                            "timestamp_seconds": 15,
                            "reaction": "Fits perfectly within a 6x3 yoga mat space with zero worry about downstairs neighbor complaints.",
                            "sentiment": "positive",
                            "suggestion": None
                        },
                        {
                            "timestamp_seconds": 580,
                            "reaction": "Reverse lunge stepping backward is much quieter than forward lunge impact.",
                            "sentiment": "positive",
                            "suggestion": None
                        }
                    ],
                    "concerns": [
                        {
                            "timestamp_seconds": 85,
                            "reaction": "Wide arm circles almost hit my living room bookshelf.",
                            "sentiment": "neutral",
                            "suggestion": "Suggest cactus-arms or elbow circles for very tight studio spaces."
                        }
                    ]
                }
            ],
            "disagreements": [
                {
                    "timestamp_seconds": 210,
                    "topic": "Squat to Calf Raise vs Jump Squat",
                    "beginner": "Loves the calf raise because jump squats cause patellar pain.",
                    "experienced": "Thinks jump squats are vastly superior for rate of force development and explosive power.",
                    "home_viewer": "100% agrees with calf raise because jump squats cause vibration and noise downstairs."
                },
                {
                    "timestamp_seconds": 750,
                    "topic": "Shadow Boxing for Cardio",
                    "beginner": "Fun, unintimidating, and gets the heart pumping easily.",
                    "experienced": "Feels it lacks progressive resistance and mechanical overload.",
                    "home_viewer": "Appreciates being able to stand quietly without stomping on hardwood floors."
                }
            ]
        },
        "shorts": [
            {
                "start_seconds": 210,
                "end_seconds": 252,
                "duration_seconds": 42,
                "title": "Burn Fat with ZERO Jumping (Apartment Friendly Cardio)",
                "hook_caption": "Downstairs neighbors hate your workouts? Do this instead 🔇",
                "reason_standalone": "Shows the triple-extension squat-to-calf-raise hack that provides HIIT burn with zero foot impact."
            },
            {
                "start_seconds": 960,
                "end_seconds": 1002,
                "duration_seconds": 42,
                "title": "The 3-Second Push-Up Secret for Explosive Chest Gains",
                "hook_caption": "Normal push-ups too easy? Try this 3-second descent 🔥",
                "reason_standalone": "Delivers a brutal bodyweight eccentric burnout demonstration that works as a stand-alone challenge."
            }
        ]
    }
}


def get_sample_by_id_or_url(url_or_id: str):
    """
    Check if a provided URL or ID matches one of our curated sample videos.
    Returns the sample dictionary if matched, or None.
    """
    if not url_or_id:
        return None

    cleaned = url_or_id.strip().lower()

    for key, sample in SAMPLE_VIDEOS.items():
        if key in cleaned:
            return sample
        if sample["youtube_url"].lower() in cleaned or sample["id"] in cleaned:
            return sample
        # Check by YouTube video ID
        yt_id = sample["youtube_url"].split("v=")[-1]
        if yt_id.lower() in cleaned:
            return sample

    return None


SAMPLE_TRANSLATIONS = {
    "tamil": {
        "target_language": "Tamil",
        "translated_summary": "ஆரம்பநிலை உடற்பயிற்சியாளர்களுக்காக வடிவமைக்கப்பட்ட ஓர் அடிப்படை முழு உடல் டம்பல் உடற்பயிற்சி; இது படிப்படியான உடல் தோரணை வழிகாட்டல்கள் மற்றும் வேகக் கட்டுப்பாட்டு வழிமுறைகளுடன் 5 கூட்டுப் பயிற்சிகளை அறிமுகப்படுத்துகிறது.",
        "translated_improvements": [
            "தற்காலிகத் தலைப்பை மாற்றி, வீடியோவை விவரிக்கும் வகையில் முக்கிய தேடல் சொற்கள் நிறைந்த கவர்ச்சிகரமான தலைப்பை வைக்கவும்.",
            "தொடக்கத்தில் வரும் 10 வினாடி நிலையான தலைப்பு அட்டைகளைத் தவிர்த்து, முதல் விநாடியிலிருந்தே பார்வையாளர்களுடன் நேரடியாகப் பேசவும்.",
            "பயிற்சியின் வேகத்தையும் இடைவெளிகளையும் சீராக வைத்திருக்க, திரையில் தெரியும் வகையிலான இடைவெளி நேரக் காட்டியைச் (interval countdown timer) சேர்க்கவும்."
        ],
        "translated_titles": [
            "வெறும் 2 டம்பல்களைக் கொண்டு முழு உடல் வலிமையை உருவாக்குங்கள் (தொடக்கநிலை பயிற்சி)",
            "ஆரம்பநிலையாளர்களுக்குத் தேவையான 5 முக்கியமான டம்பல் பயிற்சிகள் மட்டுமே (முழு உடல்)",
            "வீட்டிலேயே தொடங்குங்கள்: எளிய 15 நிமிட முழு உடல் டம்பல் பயிற்சி"
        ]
    },
    "hindi": {
        "target_language": "Hindi",
        "translated_summary": "शुरुआती लोगों के लिए डिज़ाइन किया गया एक बुनियादी फुल-बॉडी डंबल वर्कआउट, जिसमें प्रगतिशील फॉर्म संकेतों और गति निर्देशों के साथ 5 संयुक्त अभ्यास शामिल हैं।",
        "translated_improvements": [
            "प्लेसहोल्डर शीर्षक को बदलकर एक वर्णनात्मक, कीवर्ड-युक्त शीर्षक लगाएं।",
            "शुरुआती 10-सेकंड के स्थिर शीर्षक कार्ड को हटाएं और पहले सेकंड से दर्शकों से सीधे बात करें।",
            "स्क्रीन पर अंतराल उलटी गिनती टाइमर (interval timer) जोड़ें।"
        ],
        "translated_titles": [
            "सिर्फ 2 डंबल से बनाएं फुल-बॉडी स्ट्रेंथ (शुरुआती वर्कआउट)",
            "शुरुआती लोगों के लिए केवल 5 आवश्यक डंबल एक्सरसाइज (फुल बॉडी)",
            "घर पर 15 मिनट का आसान डंबल वर्कआउट"
        ]
    },
    "spanish": {
        "target_language": "Spanish",
        "translated_summary": "Un entrenamiento fundamental de cuerpo completo con mancuernas para principiantes, que introduce 5 ejercicios compuestos con pautas técnicas progresivas.",
        "translated_improvements": [
            "Reemplaza el título genérico con uno descriptivo y rico en palabras clave.",
            "Elimina las tarjetas estáticas de los primeros 10 segundos y habla directamente a la audiencia.",
            "Añade un temporizador de intervalos en pantalla durante las series."
        ],
        "translated_titles": [
            "Desarrolla Fuerza Total con solo 2 Mancuernas (Rutina Principiante)",
            "Los Únicos 5 Ejercicios con Mancuernas que Necesitas para Empezar",
            "Rutina de 15 Minutos con Mancuernas en Casa para Principiantes"
        ]
    }
}


def get_sample_translation(target_language: str):
    """
    Get pre-cached sample translation for fallback or offline demo.
    """
    if not target_language:
        return None
    key = target_language.strip().lower()
    if "tamil" in key or key == "ta":
        return SAMPLE_TRANSLATIONS.get("tamil")
    if "hindi" in key or key == "hi":
        return SAMPLE_TRANSLATIONS.get("hindi")
    if "spanish" in key or key == "es":
        return SAMPLE_TRANSLATIONS.get("spanish")
    return None


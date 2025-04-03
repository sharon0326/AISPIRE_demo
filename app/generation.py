import requests
import os

FLOWITH_API_KEY = os.getenv("FLOWITH_API_KEY")
FLOWITH_KB_LIST = [os.getenv("FLOWITH_KB_LIST")]
MODEL_USED = "gpt-4o-mini"
#MODEL_USED = 'DeepSeek-R1'
API_URL = "https://edge.flowith.net/external/use/seek-knowledge"


def fetch_flowith_response(messages):
    headers = {
        "Authorization": f"Bearer {FLOWITH_API_KEY}",
        "Content-Type": "application/json",
        "Host": "edge.flowith.net"
    }
    payload = {
        "messages": messages,
        "model": MODEL_USED,
        "stream": False,
        "kb_list": FLOWITH_KB_LIST
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        res = response.json()
        return res.get("content", "") if res.get("tag") == "final" else ""
    except Exception as e:
        print(f"Flowith API Error: {str(e)}")
        return ""

def generate_montage_outlines(notes, topic):
    system_msg = {
        "role": "system",
        "content": """You are a college essay expert specializing in montage style narratives. 
        Create cinematic outlines that weave multiple vignettes into cohesive stories using both the provided 
        notes and essay topic. Focus on thematic connections rather than chronological storytelling."""
    }

    user_prompt = f"""Generate one montage-style outline for a college application essay about: {topic}
    Incorporate these brainstorming notes: {notes}

    Please use your own discretion as an essay expert to determine what material to be used in the essay and what not, 
    as well as how to use the material to improve the structure and flow of the essay. 
    Also, this is just the main personal statement, so you can't mention what school and program I am applying for.
    
    Each outline should include:
    1. Central metaphor/visual motif
    2. 3-4 vignettes with:
       - Specific snapshot scene
       - Sensory details
       - Symbolic element
    3. Transition techniques between scenes
    4. Thematic crescendo conclusion
    5. Key visual/emotional throughlines

    Format with clear montage Framework headings and cinematic terminology."""

    user_msg = {"role": "user", "content": user_prompt}

    response = fetch_flowith_response([system_msg, user_msg])
    return parse_outlines(response) if response else []


def generate_narrative_outlines(notes, topic):
    system_msg = {
        "role": "system",
        "content": """You are a college essay expert specializing in classic narrative storytelling. 
        Create structured plot-driven outlines with clear character development and emotional resonance,
        incorporating both provided notes and the essay topic."""
    }

    user_prompt = f"""Generate a narrative outline for a college application essay about: {topic}
    Incorporate these brainstorming notes: {notes}
    
    Please use your own discretion as an essay expert to determine what material to be used in the essay and what not, 
    as well as how to use the material to improve the structure and flow of the essay. 
    Also, this is just the main personal statement, so you can't mention what school and program I am applying for.

    Each outline should include:
    1. Protagonist Setup:
       - Initial state/context
       - Core motivation
       - Inciting incident
    2. Plot Progression:
       - 3 key developmental moments
       - Central conflict/challenge
       - Turning point decision
    3. Character Evolution:
       - Skills/insights gained
       - Perspective shifts
       - Transformative actions
    4. Resolution:
       - Current manifestation of growth
       - Forward-looking reflection
    5. Narrative Devices:
       - Dialogue moments
       - Symbolic objects
       - Recurring motifs

    Format with clear story structure terminology (Exposition/Rising Action/Climax).
    Generate plain text."""

    user_msg = {"role": "user", "content": user_prompt}

    response = fetch_flowith_response([system_msg, user_msg])
    return parse_outlines(response) if response else []


def generate_full_essay(topic, notes, word_limit, outline_type, selected_outline):
    system_msg = {
        "role": "system",
        "content": f"You are a professional college essay editor. Adhere strictly to {word_limit} words and follow the {outline_type} outline structure."
    }

    additional_guidelines = (
        "CRITICAL WRITING GUIDELINES:\n"
        "1. Authenticity is paramount\n"
        "2. Show, don't just tell\n"
        "3. Avoid victim narratives\n"
        "4. Highlight personal agency\n"
        "5. Use specific, vivid details\n"
        "6. Connect personal story to broader themes\n\n"
        "TONE AND STYLE RECOMMENDATIONS:\n"
        "- Conversational yet sophisticated\n"
        "- Honest and vulnerable\n"
        "- Reflective but not overly sentimental\n"
        "- Demonstrate intellectual maturity\n\n"
        "COMMON PITFALLS TO AVOID:\n"
        "- Generic story\n"
        "- Stereotypical Chinese student representations\n"
        "- Lack of personal reflection\n\n"
        "RECOMMENDED REVISION PROCESS:\n"
        "- Write multiple drafts\n"
        "- Get feedback from diverse readers\n"
        "- Read aloud to check narrative flow\n"
        "- Ensure every paragraph serves the central narrative\n\n"
        "FINAL ADVICE:\n"
        "Your essay should reveal who you are beyond achievements - your character, resilience, and unique perspective"
    )

    user_prompt = f"""Great outlines. Please generate one {word_limit}-word essays based on the outline below. You can add necessary details if needed. {additional_guidelines}

    Generate a {word_limit}-word college application essay on {topic} using these notes:{notes}
    
    Follow this outline structure ({outline_type}): {selected_outline}
    Ensure clear flow and rigorous adherence to the outline. 
    Only output the full and holistic application essays.
    In plain text.
    """

    user_msg = {"role": "user", "content": user_prompt}

    response = fetch_flowith_response([system_msg, user_msg])
    return response if response else "Error generating essay"

def parse_outlines(text):
    outlines = []
    current = []
    for line in text.split('\n'):
        if line.startswith('Outline'):
            if current:
                outlines.append('\n'.join(current))
                current = []
        current.append(line)
    if current:
        outlines.append('\n'.join(current))
    return outlines
"""
InterviewAce Premium Design System
Color palette: Indigo #4f46e5 → Violet #8b5cf6
Font: Poppins
Features: Glass morphism, animations, micro-interactions, responsive design
"""

def get_premium_css():
    """Returns the complete premium CSS with animations, depth, and responsiveness"""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    /* === ROOT VARIABLES === */
    :root {
        --primary-indigo: #4f46e5;
        --primary-violet: #8b5cf6;
        --gradient-primary: linear-gradient(135deg, #4f46e5 0%, #8b5cf6 100%);
        --gradient-mesh: radial-gradient(circle at 20% 50%, rgba(79, 70, 229, 0.15), transparent 50%),
                         radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.15), transparent 50%);
        
        /* 3D Multi-layer shadows */
        --shadow-contact: 0 1px 3px rgba(0, 0, 0, 0.15);
        --shadow-ambient: 0 8px 32px rgba(79, 70, 229, 0.12);
        --shadow-elevated: var(--shadow-contact), var(--shadow-ambient);
        
        --shadow-contact-hover: 0 2px 6px rgba(0, 0, 0, 0.2);
        --shadow-ambient-hover: 0 16px 48px rgba(79, 70, 229, 0.2);
        --shadow-elevated-hover: var(--shadow-contact-hover), var(--shadow-ambient-hover);
        
        --shadow-pressed: inset 0 2px 4px rgba(0, 0, 0, 0.15);
        
        /* Ambient glows */
        --glow-primary: 0 0 40px rgba(79, 70, 229, 0.4);
        --glow-violet: 0 0 40px rgba(139, 92, 246, 0.4);
        --glow-accent: 0 0 60px rgba(139, 92, 246, 0.5);
        
        /* Glass effects */
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.15);
        --glass-blur: blur(20px);
        
        /* Specular highlights */
        --specular-light: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, transparent 50%);
        --inner-highlight: inset 0 1px 0 rgba(255, 255, 255, 0.15), inset 0 -1px 0 rgba(0, 0, 0, 0.1);
        
        /* Animations */
        --transition-smooth: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-lift: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
        --transition-press: all 0.15s cubic-bezier(0.4, 0, 0.6, 1);
    }
    
    /* === ANIMATIONS === */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(79, 70, 229, 0.3); }
        50% { box-shadow: 0 0 40px rgba(139, 92, 246, 0.6); }
    }
    
    @keyframes progressFill {
        from { width: 0; }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    
    /* === GLOBAL STYLES === */
    * {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 25%, #2d1b4e 60%, #1e3a5f 100%);
        position: relative;
    }
    
    /* Animated mesh background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: var(--gradient-mesh);
        z-index: 0;
        pointer-events: none;
        animation: float 20s ease-in-out infinite;
    }
    
    .stApp > div {
        position: relative;
        z-index: 1;
    }

    
    /* === GLASS NAVBAR === */
    .glass-navbar {
        width: 100vw;
        margin-left: calc(-50vw + 50%);
        margin-right: calc(-50vw + 50%);
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(139, 92, 246, 0.08));
        backdrop-filter: var(--glass-blur);
        -webkit-backdrop-filter: var(--glass-blur);
        border-bottom: 1px solid var(--glass-border);
        height: clamp(60px, 10vh, 85px);
        display: flex;
        align-items: center;
        justify-content: center;
        position: sticky;
        top: 0;
        z-index: 999;
        box-shadow: var(--shadow-elevated), 
                    0 0 60px rgba(79, 70, 229, 0.15);
        animation: fadeIn 0.6s ease-out;
    }
    
    .glass-navbar::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        pointer-events: none;
    }
    
    .navbar-title {
        font-size: clamp(1.5rem, 4vw, 2.2rem);
        font-weight: 800;
        letter-spacing: 1px;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        transition: var(--transition-smooth);
        position: relative;
        filter: drop-shadow(var(--glow-primary));
    }
    
    .navbar-title::after {
        content: '';
        position: absolute;
        top: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        height: 30px;
        background: radial-gradient(ellipse, rgba(139, 92, 246, 0.4), transparent 70%);
        filter: blur(15px);
        z-index: -1;
        opacity: 0.6;
    }
    
    .navbar-title:hover {
        letter-spacing: 2px;
        transform: scale(1.02);
        filter: drop-shadow(var(--glow-accent));
    }

    
    /* === HERO SECTION === */
    .hero {
        position: relative;
        padding: clamp(2rem, 6vw, 6rem) clamp(1rem, 3vw, 3rem);
        text-align: center;
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -25%;
        width: 150%;
        height: 200%;
        background: radial-gradient(circle, rgba(79, 70, 229, 0.2) 0%, transparent 70%);
        animation: float 15s ease-in-out infinite;
        z-index: -1;
        filter: blur(60px);
    }
    
    .hero::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: var(--specular-light);
        pointer-events: none;
        opacity: 0.3;
    }
    
    .hero h1 {
        font-size: clamp(2rem, 6vw, 4rem);
        font-weight: 900;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        line-height: 1.2;
        animation: fadeInUp 0.8s ease-out 0.2s both;
        filter: drop-shadow(0 4px 20px rgba(79, 70, 229, 0.4));
        position: relative;
    }
    
    .hero h1::before {
        content: '';
        position: absolute;
        top: -20px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        height: 40px;
        background: radial-gradient(ellipse, rgba(139, 92, 246, 0.5), transparent 70%);
        filter: blur(25px);
        z-index: -1;
    }
    
    .hero p {
        font-size: clamp(1rem, 2.5vw, 1.25rem);
        color: rgba(255, 255, 255, 0.9);
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
        animation: fadeInUp 0.8s ease-out 0.4s both;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }

    
    /* === CARDS === */
    .card {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.08), rgba(139, 92, 246, 0.05));
        backdrop-filter: var(--glass-blur);
        -webkit-backdrop-filter: var(--glass-blur);
        border: 1px solid var(--glass-border);
        border-radius: clamp(16px, 2vw, 24px);
        padding: clamp(1.5rem, 3vw, 3rem);
        box-shadow: var(--shadow-elevated);
        transition: var(--transition-lift);
        animation: fadeInUp 0.6s ease-out both;
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
    }
    
    /* Inner highlight for 3D beveled effect */
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: inherit;
        box-shadow: var(--inner-highlight);
        pointer-events: none;
        z-index: 1;
    }
    
    /* Specular highlight */
    .card::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: var(--specular-light);
        pointer-events: none;
        opacity: 0.5;
        transition: opacity 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-8px) scale(1.01) perspective(1000px) rotateX(1deg);
        box-shadow: var(--shadow-elevated-hover);
        border-color: rgba(139, 92, 246, 0.4);
    }
    
    .card:hover::after {
        opacity: 0.8;
    }

    
    /* === FEATURE BOXES === */
    .feature-box {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.12), rgba(139, 92, 246, 0.08));
        backdrop-filter: var(--glass-blur);
        -webkit-backdrop-filter: var(--glass-blur);
        border: 1px solid var(--glass-border);
        border-radius: clamp(16px, 2vw, 20px);
        padding: clamp(1.5rem, 3vw, 2.5rem);
        text-align: center;
        box-shadow: var(--shadow-elevated);
        transition: var(--transition-lift);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out both;
        transform-style: preserve-3d;
    }
    
    .feature-box:nth-child(1) { animation-delay: 0.1s; }
    .feature-box:nth-child(2) { animation-delay: 0.2s; }
    .feature-box:nth-child(3) { animation-delay: 0.3s; }
    .feature-box:nth-child(4) { animation-delay: 0.4s; }
    .feature-box:nth-child(5) { animation-delay: 0.5s; }
    .feature-box:nth-child(6) { animation-delay: 0.6s; }
    
    /* Inner bevel highlight */
    .feature-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: inherit;
        box-shadow: var(--inner-highlight);
        pointer-events: none;
        z-index: 2;
    }
    
    /* Specular highlight */
    .feature-box::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 150%;
        height: 150%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        pointer-events: none;
        transition: transform 0.6s ease, opacity 0.6s ease;
        opacity: 0;
    }
    
    .feature-box:hover {
        transform: translateY(-10px) scale(1.02) perspective(1000px) rotateX(2deg);
        box-shadow: var(--shadow-elevated-hover), var(--glow-violet);
        border-color: var(--primary-violet);
    }
    
    .feature-box:hover::after {
        opacity: 1;
        transform: translate(20%, 20%);
    }

    
    .feature-box h3 {
        position: relative;
        z-index: 1;
        font-size: clamp(1.2rem, 2.5vw, 1.5rem);
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.75rem;
        transition: var(--transition-smooth);
    }
    
    .feature-box p {
        position: relative;
        z-index: 1;
        font-size: clamp(0.9rem, 1.8vw, 1rem);
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
    }
    
    .feature-box:hover h3 {
        transform: translateY(-2px);
        color: #ffffff;
    }
    
    /* === TECH BADGES === */
    .tech-badge {
        display: inline-block;
        padding: clamp(0.5rem, 1.5vw, 0.75rem) clamp(1rem, 2.5vw, 1.5rem);
        background: var(--gradient-primary);
        color: white;
        border-radius: 50px;
        font-weight: 600;
        font-size: clamp(0.85rem, 1.5vw, 1rem);
        box-shadow: var(--shadow-elevated), var(--glow-primary);
        transition: var(--transition-lift);
        margin: 0.5rem;
        animation: fadeIn 0.6s ease-out both;
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
    }
    
    /* Inner highlight for 3D pill effect */
    .tech-badge::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 50%;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.2), transparent);
        border-radius: 50px 50px 0 0;
        pointer-events: none;
    }
    
    /* Specular highlight sweep */
    .tech-badge::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 50%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.6s ease;
    }
    
    .tech-badge:hover {
        transform: scale(1.1) translateY(-3px) perspective(500px) rotateX(5deg);
        box-shadow: var(--shadow-elevated-hover), var(--glow-accent);
    }
    
    .tech-badge:hover::after {
        left: 150%;
    }

    
    /* === STREAMLIT BUTTONS === */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 12px;
        padding: clamp(0.7rem, 1.5vw, 1rem) clamp(1.5rem, 3vw, 2.5rem);
        font-weight: 600;
        font-size: clamp(0.9rem, 1.8vw, 1.05rem);
        letter-spacing: 0.5px;
        box-shadow: var(--shadow-elevated), var(--glow-primary);
        transition: var(--transition-press);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        min-height: 44px;
        transform-style: preserve-3d;
    }
    
    /* Inner bevel for 3D raised effect */
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: inherit;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.3), 
                    inset 0 -1px 0 rgba(0, 0, 0, 0.15);
        pointer-events: none;
    }
    
    /* Specular highlight */
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 0;
        left: -50%;
        width: 200%;
        height: 100%;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(255, 255, 255, 0) 100%);
        transform: translateX(-100%);
        transition: transform 0.6s ease;
        pointer-events: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: var(--shadow-elevated-hover), var(--glow-accent);
    }
    
    .stButton > button:hover::after {
        transform: translateX(100%);
    }
    
    /* Pressed state - button depresses like real button */
    .stButton > button:active {
        transform: translateY(0px) scale(0.98);
        box-shadow: var(--shadow-pressed), 
                    0 4px 12px rgba(79, 70, 229, 0.2);
    }
    
    .stButton > button:active::before {
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    
    /* === INPUTS === */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(79, 70, 229, 0.03));
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        color: white;
        padding: clamp(0.7rem, 1.5vw, 0.9rem);
        font-size: clamp(0.9rem, 1.8vw, 1rem);
        box-shadow: var(--shadow-contact), 
                    inset 0 1px 2px rgba(0, 0, 0, 0.1);
        transition: var(--transition-smooth);
        position: relative;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary-violet);
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2),
                    var(--shadow-elevated),
                    inset 0 1px 2px rgba(0, 0, 0, 0.1);
        background: rgba(255, 255, 255, 0.08);
        outline: none;
        transform: translateY(-1px);
    }
    
    /* Radio buttons */
    .stRadio > div {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.05);
        padding: clamp(0.6rem, 1.5vw, 0.8rem) clamp(1.2rem, 2.5vw, 1.8rem);
        border-radius: 50px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: var(--transition-smooth);
        cursor: pointer;
        min-height: 44px; /* Touch target */
        display: flex;
        align-items: center;
    }
    
    .stRadio > div > label:hover {
        background: rgba(139, 92, 246, 0.2);
        border-color: var(--primary-violet);
        transform: translateY(-2px);
    }

    
    /* === SLIDER === */
    .stSlider > div > div > div {
        background: var(--gradient-primary);
    }
    
    /* === PROGRESS BAR === */
    .stProgress > div > div > div {
        background: var(--gradient-primary);
        animation: progressFill 1.5s ease-out;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
    }
    
    /* === METRICS === */
    .stMetric {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.08), rgba(139, 92, 246, 0.05));
        backdrop-filter: var(--glass-blur);
        padding: clamp(1rem, 2vw, 1.5rem);
        border-radius: 12px;
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-elevated);
        transition: var(--transition-lift);
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .stMetric::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: inherit;
        box-shadow: var(--inner-highlight);
        pointer-events: none;
    }
    
    .stMetric::after {
        content: '';
        position: absolute;
        top: -20px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        height: 30px;
        background: radial-gradient(ellipse, rgba(139, 92, 246, 0.4), transparent 70%);
        filter: blur(15px);
        z-index: -1;
    }
    
    .stMetric:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: var(--shadow-elevated-hover), var(--glow-violet);
        border-color: var(--primary-violet);
    }
    
    .stMetric label {
        font-size: clamp(0.9rem, 1.8vw, 1rem);
        color: rgba(255, 255, 255, 0.8);
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: clamp(1.5rem, 3vw, 2.5rem);
        font-weight: 700;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 2px 8px rgba(79, 70, 229, 0.3));
    }

    
    /* === EXPANDERS === */
    .stExpander {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        box-shadow: var(--shadow-subtle);
        transition: var(--transition-smooth);
        margin: 0.5rem 0;
    }
    
    .stExpander:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(139, 92, 246, 0.3);
    }
    
    .stExpander summary {
        padding: 1rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.9);
        cursor: pointer;
        transition: var(--transition-smooth);
    }
    
    .stExpander summary:hover {
        color: var(--primary-violet);
    }
    
    /* === TYPOGRAPHY === */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        font-weight: 700;
        line-height: 1.3;
    }
    
    h1 { font-size: clamp(2rem, 5vw, 3rem); }
    h2 { font-size: clamp(1.5rem, 4vw, 2.25rem); }
    h3 { font-size: clamp(1.25rem, 3vw, 1.75rem); }
    
    p, li, label {
        color: rgba(255, 255, 255, 0.85);
        line-height: 1.6;
    }
    
    /* Animated links */
    a {
        color: var(--primary-violet);
        text-decoration: none;
        position: relative;
        transition: var(--transition-smooth);
    }
    
    a::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 0;
        height: 2px;
        background: var(--gradient-primary);
        transition: width 0.3s ease;
    }
    
    a:hover::after {
        width: 100%;
    }

    
    /* === RESPONSIVE BREAKPOINTS === */
    
    /* Tablets and below (1024px) */
    @media (max-width: 1024px) {
        .glass-navbar {
            height: 70px;
        }
        
        .navbar-title {
            font-size: 1.8rem;
        }
        
        .hero {
            padding: 3rem 1.5rem;
        }
        
        .card, .feature-box {
            padding: 2rem;
        }
        
        .stButton > button {
            padding: 0.8rem 2rem;
        }
    }
    
    /* Mobile landscape (768px) */
    @media (max-width: 768px) {
        .glass-navbar {
            height: 65px;
        }
        
        .navbar-title {
            font-size: 1.5rem;
            letter-spacing: 0.5px;
        }
        
        .hero {
            padding: 2.5rem 1rem;
        }
        
        .hero h1 {
            font-size: 2rem;
        }
        
        .hero p {
            font-size: 1rem;
        }
        
        .card, .feature-box {
            padding: 1.5rem;
            margin: 0.75rem 0;
        }
        
        .tech-badge {
            padding: 0.5rem 1rem;
            font-size: 0.85rem;
            margin: 0.3rem;
        }
        
        .stButton > button {
            width: 100%;
            padding: 0.9rem 1.5rem;
        }
        
        /* Stack columns on mobile */
        .row-widget.stHorizontal {
            flex-direction: column;
        }
    }

    
    /* Mobile portrait (480px) */
    @media (max-width: 480px) {
        .glass-navbar {
            height: 60px;
        }
        
        .navbar-title {
            font-size: 1.3rem;
        }
        
        .hero {
            padding: 2rem 0.75rem;
        }
        
        .hero h1 {
            font-size: 1.75rem;
            margin-bottom: 1rem;
        }
        
        .hero p {
            font-size: 0.95rem;
        }
        
        .card, .feature-box {
            padding: 1.25rem;
            border-radius: 12px;
        }
        
        .feature-box h3 {
            font-size: 1.1rem;
        }
        
        .feature-box p {
            font-size: 0.9rem;
        }
        
        .tech-badge {
            padding: 0.4rem 0.8rem;
            font-size: 0.8rem;
        }
        
        .stButton > button {
            font-size: 0.95rem;
            padding: 0.85rem 1.25rem;
        }
    }
    
    /* === UTILITIES === */
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .slide-in-left {
        animation: slideInLeft 0.6s ease-out;
    }
    
    /* Hidden scrollbar for cleaner look */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gradient-primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #8b5cf6 0%, #4f46e5 100%);
    }
    
    </style>
    """


def get_glass_navbar(title="InterviewAce"):
    """Returns a glass-morphism navbar with the title"""
    return f"""
    <div class='glass-navbar'>
        <div class='navbar-title'>{title}</div>
    </div>
    """

def get_hero_section(title, subtitle):
    """Returns an animated hero section"""
    return f"""
    <div class='hero'>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """


def get_styled_accordion_css():
    """Returns CSS for styled accordion/expander sections"""
    return """
    <style>
    /* === STYLED ACCORDIONS === */
    .stExpander {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 12px !important;
        margin: 0.75rem 0 !important;
        overflow: hidden !important;
        transition: var(--transition-smooth) !important;
    }
    
    .stExpander:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: var(--primary-violet) !important;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2) !important;
    }
    
    .stExpander summary {
        background: transparent !important;
        padding: 1rem 1.25rem !important;
        font-weight: 600 !important;
        color: rgba(255, 255, 255, 0.95) !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        transition: var(--transition-smooth) !important;
    }
    
    .stExpander summary:hover {
        background: rgba(139, 92, 246, 0.1) !important;
        color: #ffffff !important;
    }
    
    .stExpander[open] summary {
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(79, 70, 229, 0.15) !important;
    }
    
    /* Chevron icon animation */
    .stExpander summary::before {
        content: '›' !important;
        font-size: 1.5rem !important;
        margin-right: 0.75rem !important;
        transition: transform 0.3s ease !important;
        display: inline-block !important;
        color: var(--primary-violet) !important;
    }
    
    .stExpander[open] summary::before {
        transform: rotate(90deg) !important;
    }
    
    .stExpander > div:last-child {
        padding: 1.25rem !important;
        background: rgba(0, 0, 0, 0.2) !important;
    }
    </style>
    """


def get_stat_card_css():
    """Returns CSS for stat cards with category-specific colors"""
    return """
    <style>
    /* === STAT CARDS === */
    .stat-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.25rem;
        margin: 1.5rem 0;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .stat-card {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.08), rgba(139, 92, 246, 0.05));
        backdrop-filter: var(--glass-blur);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-elevated);
        transition: var(--transition-lift);
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
    }
    
    /* Inner bevel */
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: inherit;
        box-shadow: var(--inner-highlight);
        pointer-events: none;
        z-index: 2;
    }
    
    /* Accent bar with glow */
    .stat-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--accent-color);
        box-shadow: 0 0 20px var(--accent-color);
        transition: width 0.3s ease, box-shadow 0.3s ease;
        z-index: 1;
    }
    
    .stat-card:hover {
        transform: translateY(-8px) scale(1.02) perspective(1000px) rotateX(2deg);
        border-color: var(--accent-color);
        box-shadow: var(--shadow-elevated-hover), 
                    0 0 40px rgba(var(--accent-rgb), 0.4);
    }
    
    .stat-card:hover::after {
        width: 100%;
        opacity: 0.15;
    }
    
    .stat-card-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
        position: relative;
        z-index: 3;
    }
    
    .stat-card-label {
        font-size: 0.9rem;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.8);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 3;
    }
    
    .stat-card-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--accent-color);
        line-height: 1;
        filter: drop-shadow(0 2px 10px rgba(var(--accent-rgb), 0.5));
        position: relative;
        z-index: 3;
    }
    
    /* Category-specific colors with RGB values for transparency */
    .stat-strengths { 
        --accent-color: #10b981; 
        --accent-rgb: 16, 185, 129;
    }
    .stat-weaknesses { 
        --accent-color: #ef4444; 
        --accent-rgb: 239, 68, 68;
    }
    .stat-communication { 
        --accent-color: #3b82f6; 
        --accent-rgb: 59, 130, 246;
    }
    .stat-technical { 
        --accent-color: #8b5cf6; 
        --accent-rgb: 139, 92, 246;
    }
    .stat-overall { 
        --accent-color: #f59e0b; 
        --accent-rgb: 245, 158, 11;
    }
    
    @media (max-width: 768px) {
        .stat-card-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
    }
    </style>
    """


def get_empty_state_css():
    """Returns CSS for empty state messages"""
    return """
    <style>
    /* === EMPTY STATES === */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(255, 255, 255, 0.03);
        border: 2px dashed rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        margin: 2rem 0;
        animation: fadeIn 0.6s ease-out;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        opacity: 0.5;
        animation: float 3s ease-in-out infinite;
    }
    
    .empty-state-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 0.75rem;
    }
    
    .empty-state-message {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.6);
        max-width: 400px;
        margin: 0 auto;
        line-height: 1.6;
    }
    </style>
    """


def get_skeleton_loader_css():
    """Returns CSS for skeleton loading animation"""
    return """
    <style>
    /* === SKELETON LOADER === */
    .skeleton-loader {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.05), rgba(139, 92, 246, 0.03));
        backdrop-filter: var(--glass-blur);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-elevated);
    }
    
    .skeleton-loader::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(139, 92, 246, 0.3),
            transparent
        );
        animation: shimmer 2s infinite;
    }
    
    .skeleton-line {
        height: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        margin: 0.75rem 0;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .skeleton-line.short {
        width: 60%;
    }
    
    .skeleton-line.medium {
        width: 80%;
    }
    
    .skeleton-line.long {
        width: 100%;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .loading-indicator {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.12), rgba(139, 92, 246, 0.08));
        backdrop-filter: var(--glass-blur);
        border-radius: 16px;
        border: 1px solid var(--glass-border);
        margin: 1.5rem 0;
        box-shadow: var(--shadow-elevated), var(--glow-primary);
        position: relative;
    }
    
    .loading-indicator::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: inherit;
        box-shadow: var(--inner-highlight);
        pointer-events: none;
    }
    
    .loading-spinner {
        width: 24px;
        height: 24px;
        border: 3px solid rgba(139, 92, 246, 0.3);
        border-top-color: var(--primary-violet);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        filter: drop-shadow(0 0 8px rgba(139, 92, 246, 0.6));
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-weight: 600;
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.05rem;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    </style>
    """


def get_navigation_css():
    """Returns CSS for active page navigation and step indicators"""
    return """
    <style>
    /* === NAVIGATION === */
    .page-nav {
        display: flex;
        gap: 0.5rem;
        justify-content: center;
        margin: 1rem 0 2rem 0;
        flex-wrap: wrap;
    }
    
    .page-nav-item {
        padding: 0.6rem 1.5rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(79, 70, 229, 0.05));
        backdrop-filter: var(--glass-blur);
        border: 1px solid var(--glass-border);
        border-radius: 50px;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
        font-size: 0.95rem;
        transition: var(--transition-lift);
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        box-shadow: var(--shadow-contact);
        position: relative;
    }
    
    .page-nav-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 50%;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.1), transparent);
        border-radius: 50px 50px 0 0;
        pointer-events: none;
    }
    
    .page-nav-item:hover {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(79, 70, 229, 0.15));
        border-color: var(--primary-violet);
        color: #ffffff;
        transform: translateY(-2px) scale(1.02);
        box-shadow: var(--shadow-elevated);
    }
    
    .page-nav-item.active {
        background: var(--gradient-primary);
        border-color: var(--primary-violet);
        color: #ffffff;
        box-shadow: var(--shadow-elevated), var(--glow-primary);
        transform: scale(1.05);
    }
    
    /* === STEP INDICATOR === */
    .step-indicator {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin: 2rem 0;
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.05), rgba(139, 92, 246, 0.03));
        backdrop-filter: var(--glass-blur);
        border-radius: 16px;
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-elevated);
        position: relative;
    }
    
    .step-indicator::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: inherit;
        box-shadow: var(--inner-highlight);
        pointer-events: none;
    }
    
    .step {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(79, 70, 229, 0.08));
        border: 2px solid rgba(255, 255, 255, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.7);
        transition: var(--transition-lift);
        box-shadow: var(--shadow-contact), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
    }
    
    .step.active .step-circle {
        background: var(--gradient-primary);
        border-color: var(--primary-violet);
        color: #ffffff;
        box-shadow: var(--shadow-elevated), var(--glow-accent);
        transform: scale(1.15);
    }
    
    .step.active .step-circle::before {
        content: '';
        position: absolute;
        inset: -10px;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.4), transparent 70%);
        border-radius: 50%;
        z-index: -1;
        filter: blur(15px);
    }
    
    .step.completed .step-circle {
        background: linear-gradient(135deg, #10b981, #059669);
        border-color: #10b981;
        color: #ffffff;
        box-shadow: var(--shadow-elevated), 
                    0 0 20px rgba(16, 185, 129, 0.4);
    }
    
    .step.completed .step-circle::before {
        content: '✓';
    }
    
    .step-label {
        font-weight: 600;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        display: none;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }
    
    .step.active .step-label {
        color: #ffffff;
    }
    
    .step-arrow {
        color: rgba(255, 255, 255, 0.3);
        font-size: 1.5rem;
    }
    
    @media (min-width: 768px) {
        .step-label {
            display: block;
        }
        
        .step-circle {
            width: 50px;
            height: 50px;
        }
    }
    </style>
    """


def get_accessibility_css():
    """Returns CSS for accessibility improvements (WCAG AA, focus states, etc.)"""
    return """
    <style>
    /* === ACCESSIBILITY === */
    
    /* Focus states for keyboard navigation */
    .stButton > button:focus,
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stSelectbox select:focus,
    .stRadio label:focus-within {
        outline: 3px solid var(--primary-violet) !important;
        outline-offset: 2px !important;
        box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.2) !important;
    }
    
    .page-nav-item:focus {
        outline: 3px solid var(--primary-violet);
        outline-offset: 2px;
        box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.2);
    }
    
    .feature-box:focus {
        outline: 3px solid var(--primary-violet);
        outline-offset: 4px;
    }
    
    /* Improved color contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    p, li, label, span {
        color: rgba(255, 255, 255, 0.95) !important;
    }
    
    .stMarkdown {
        color: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* High contrast borders for better visibility */
    input, textarea, select {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Focus visible for all interactive elements */
    *:focus-visible {
        outline: 3px solid var(--primary-violet) !important;
        outline-offset: 2px !important;
    }
    
    /* Skip to content link (hidden but accessible) */
    .skip-to-content {
        position: absolute;
        top: -40px;
        left: 0;
        background: var(--primary-violet);
        color: white;
        padding: 8px 16px;
        text-decoration: none;
        border-radius: 0 0 4px 0;
        z-index: 10000;
    }
    
    .skip-to-content:focus {
        top: 0;
    }
    
    /* Ensure minimum touch targets */
    button, a, input, select, textarea {
        min-height: 44px !important;
        min-width: 44px !important;
    }
    
    /* Reduced motion support */
    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    </style>
    """


def get_complete_theme():
    """Returns the complete theme with all components"""
    return (
        get_premium_css() + 
        get_styled_accordion_css() + 
        get_stat_card_css() + 
        get_empty_state_css() + 
        get_skeleton_loader_css() + 
        get_navigation_css() + 
        get_accessibility_css()
    )

def get_empty_state(icon, title, message):
    """Returns an empty state component"""
    return f"""
    <div class='empty-state'>
        <div class='empty-state-icon'>{icon}</div>
        <div class='empty-state-title'>{title}</div>
        <div class='empty-state-message'>{message}</div>
    </div>
    """

def get_loading_indicator(message="Generating..."):
    """Returns a loading indicator with skeleton shimmer"""
    return f"""
    <div class='loading-indicator'>
        <div class='loading-spinner'></div>
        <div class='loading-text'>{message}</div>
    </div>
    """

def get_skeleton_loader(lines=3):
    """Returns a skeleton loader"""
    skeleton_lines = ""
    for i in range(lines):
        width = ["short", "medium", "long"][i % 3]
        skeleton_lines += f"<div class='skeleton-line {width}'></div>"
    
    return f"""
    <div class='skeleton-loader'>
        {skeleton_lines}
    </div>
    """

def get_stat_card(icon, label, value, category):
    """Returns a stat card component"""
    return f"""
    <div class='stat-card stat-{category}'>
        <div class='stat-card-icon'>{icon}</div>
        <div class='stat-card-label'>{label}</div>
        <div class='stat-card-value'>{value}</div>
    </div>
    """

def get_step_indicator(steps, current_step):
    """
    Returns a step indicator component
    steps: list of step names
    current_step: index of current step (0-based)
    """
    html = "<div class='step-indicator'>"
    
    for i, step in enumerate(steps):
        state = "completed" if i < current_step else ("active" if i == current_step else "")
        
        html += f"""
        <div class='step {state}'>
            <div class='step-circle'>{'' if i < current_step else i + 1}</div>
            <div class='step-label'>{step}</div>
        </div>
        """
        
        if i < len(steps) - 1:
            html += "<div class='step-arrow'>→</div>"
    
    html += "</div>"
    return html

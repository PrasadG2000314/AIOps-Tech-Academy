from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AIOps Tech Store & Academy | Software Engineering & Cloud Solutions</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Space+Grotesk:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <!-- Lucide Icons & Canvas Confetti -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        :root {
            --bg-primary: #06080e;
            --bg-secondary: #0b0f19;
            --bg-card: rgba(14, 20, 36, 0.75);
            --bg-card-hover: rgba(22, 32, 58, 0.85);
            --border-glass: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(59, 130, 246, 0.5);
            
            --accent-cyan: #00f2fe;
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-pink: #ec4899;
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-orange: #f97316;
            
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            
            --radius-sm: 8px;
            --radius-md: 14px;
            --radius-lg: 20px;
            --radius-full: 9999px;
            
            --shadow-card: 0 10px 30px -10px rgba(0, 0, 0, 0.6);
            --shadow-glow-cyan: 0 0 35px rgba(0, 242, 254, 0.25);
            --shadow-glow-blue: 0 0 35px rgba(59, 130, 246, 0.25);
            --shadow-glow-purple: 0 0 35px rgba(139, 92, 246, 0.25);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-font-smoothing: antialiased;
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            overflow-x: hidden;
            display: flex;
            flex-direction: column;
        }

        /* Ambient Background Grid & Floating Lights */
        .bg-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -3;
            background: 
                radial-gradient(circle at 10% 15%, rgba(59, 130, 246, 0.12) 0%, transparent 45%),
                radial-gradient(circle at 90% 25%, rgba(139, 92, 246, 0.15) 0%, transparent 45%),
                radial-gradient(circle at 50% 85%, rgba(0, 242, 254, 0.08) 0%, transparent 55%),
                #06080e;
        }

        .grid-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -2;
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
            background-size: 50px 50px;
            mask-image: radial-gradient(circle at 50% 50%, black 50%, transparent 90%);
            -webkit-mask-image: radial-gradient(circle at 50% 50%, black 50%, transparent 90%);
            pointer-events: none;
        }

        .orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(90px);
            opacity: 0.45;
            animation: orbFloat 20s ease-in-out infinite alternate;
            pointer-events: none;
            z-index: -1;
        }
        .orb-1 { width: 500px; height: 500px; background: #2563eb; top: -150px; left: -150px; }
        .orb-2 { width: 450px; height: 450px; background: #8b5cf6; top: 35%; right: -120px; animation-delay: -6s; }
        .orb-3 { width: 400px; height: 400px; background: #00f2fe; bottom: 5%; left: 10%; animation-delay: -12s; }

        @keyframes orbFloat {
            0% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(60px, 80px) scale(1.08); }
            100% { transform: translate(-50px, 120px) scale(0.92); }
        }

        /* 1. Sticky System Status Bar */
        .status-bar-wrapper {
            background: rgba(6, 10, 20, 0.88);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-bottom: 1px solid rgba(16, 185, 129, 0.22);
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .status-bar {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0.55rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 0.825rem;
            font-weight: 600;
        }

        .status-left {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: #86efac;
        }

        .pulse-beacon {
            position: relative;
            width: 10px;
            height: 10px;
            background-color: var(--accent-green);
            border-radius: 50%;
        }

        .pulse-beacon::after {
            content: '';
            position: absolute;
            top: -4px; left: -4px; right: -4px; bottom: -4px;
            border-radius: 50%;
            background-color: rgba(16, 185, 129, 0.6);
            animation: pulseRipple 1.8s cubic-bezier(0, 0, 0.2, 1) infinite;
        }

        @keyframes pulseRipple {
            0% { transform: scale(0.8); opacity: 1; }
            100% { transform: scale(2.6); opacity: 0; }
        }

        .status-metrics {
            display: flex;
            align-items: center;
            gap: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .metric-pill {
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .metric-pill span.val {
            color: #38bdf8;
            font-weight: 700;
        }

        /* 2. Main Navigation Bar */
        .navbar-wrapper {
            background: rgba(9, 14, 26, 0.75);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-glass);
            position: sticky;
            top: 36px;
            z-index: 990;
        }

        .navbar {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0.85rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .brand-logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
            color: var(--text-main);
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.35rem;
            font-weight: 700;
            cursor: pointer;
        }

        .brand-icon {
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, #2563eb, #8b5cf6);
            border-radius: var(--radius-sm);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
        }

        .brand-badge {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2));
            border: 1px solid rgba(139, 92, 246, 0.4);
            color: #c084fc;
            padding: 0.2rem 0.5rem;
            border-radius: var(--radius-sm);
            font-size: 0.68rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            letter-spacing: 0.05em;
        }

        .nav-links {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            list-style: none;
        }

        .nav-item {
            padding: 0.55rem 1rem;
            border-radius: var(--radius-full);
            color: var(--text-muted);
            font-size: 0.9rem;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.25s ease;
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }

        .nav-item svg {
            width: 16px;
            height: 16px;
        }

        .nav-item:hover {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.06);
        }

        .nav-item.active {
            color: #ffffff;
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.3), rgba(124, 58, 237, 0.3));
            border: 1px solid rgba(59, 130, 246, 0.4);
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.2);
        }

        .nav-actions {
            display: flex;
            align-items: center;
            gap: 0.85rem;
        }

        .cart-trigger-btn {
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            color: var(--text-main);
            padding: 0.6rem 1.15rem;
            border-radius: var(--radius-full);
            display: flex;
            align-items: center;
            gap: 0.55rem;
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .cart-trigger-btn:hover {
            border-color: var(--accent-blue);
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.35);
            transform: translateY(-1px);
        }

        .cart-count-badge {
            background: linear-gradient(135deg, #ec4899, #f43f5e);
            color: white;
            font-size: 0.72rem;
            font-weight: 800;
            padding: 0.15rem 0.45rem;
            border-radius: var(--radius-full);
            min-width: 18px;
            text-align: center;
        }

        .cart-bump { animation: bump 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
        @keyframes bump { 0% { transform: scale(1); } 50% { transform: scale(1.35); } 100% { transform: scale(1); } }

        /* Main Container Views */
        .view-container {
            display: none;
            max-width: 1400px;
            margin: 0 auto;
            padding: 2.5rem 1.5rem 5rem;
            width: 100%;
            flex-grow: 1;
            animation: fadeInView 0.4s ease forwards;
        }

        .view-container.active {
            display: block;
        }

        @keyframes fadeInView {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Hero Banner Section */
        .hero {
            text-align: center;
            padding: 2.5rem 1rem 3.5rem;
            max-width: 960px;
            margin: 0 auto;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(59, 130, 246, 0.12);
            border: 1px solid rgba(59, 130, 246, 0.35);
            color: #93c5fd;
            padding: 0.45rem 1.15rem;
            border-radius: var(--radius-full);
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
        }

        .hero h1 {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(2.3rem, 5.5vw, 3.85rem);
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 1.1rem;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, #ffffff 20%, #93c5fd 60%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero p.subtitle {
            font-size: 1.2rem;
            color: var(--text-muted);
            font-weight: 400;
            max-width: 720px;
            margin: 0 auto 2rem;
            line-height: 1.65;
        }

        /* Search & Filter Bar */
        .search-filter-wrapper {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 2.5rem;
            background: rgba(14, 20, 36, 0.5);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-lg);
            padding: 0.75rem 1rem;
        }

        .search-box {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-full);
            padding: 0.5rem 1rem;
            min-width: 280px;
            flex-grow: 1;
            max-width: 420px;
        }

        .search-box input {
            background: transparent;
            border: none;
            color: var(--text-main);
            font-size: 0.9rem;
            outline: none;
            width: 100%;
        }

        .filters-group {
            display: flex;
            gap: 0.4rem;
            flex-wrap: wrap;
        }

        .filter-btn {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-glass);
            color: var(--text-muted);
            padding: 0.5rem 1.1rem;
            border-radius: var(--radius-full);
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .filter-btn:hover {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.08);
        }

        .filter-btn.active {
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            color: #ffffff;
            border-color: transparent;
            box-shadow: 0 0 18px rgba(59, 130, 246, 0.35);
        }

        /* Products & Courses Grid Layout */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }

        /* Premium Card Component */
        .premium-card {
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-radius: var(--radius-lg);
            padding: 2rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .premium-card:hover {
            transform: translateY(-8px);
            border-color: var(--border-glow);
            box-shadow: var(--shadow-card), var(--shadow-glow-blue);
        }

        .card-header-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1.25rem;
        }

        .card-icon-box {
            width: 56px;
            height: 56px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.04);
            transition: transform 0.3s ease;
        }

        .premium-card:hover .card-icon-box {
            transform: scale(1.1) rotate(-3deg);
        }

        .card-badge {
            font-size: 0.72rem;
            font-weight: 700;
            padding: 0.3rem 0.7rem;
            border-radius: var(--radius-full);
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }

        .badge-cyan { background: rgba(0, 242, 254, 0.12); color: #38bdf8; border: 1px solid rgba(0, 242, 254, 0.3); }
        .badge-pink { background: rgba(236, 72, 153, 0.12); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.3); }
        .badge-green { background: rgba(16, 185, 129, 0.12); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.3); }
        .badge-purple { background: rgba(139, 92, 246, 0.12); color: #c084fc; border: 1px solid rgba(139, 92, 246, 0.3); }
        .badge-amber { background: rgba(245, 158, 11, 0.12); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }

        .card-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.45rem;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 0.6rem;
            letter-spacing: -0.02em;
        }

        .card-desc {
            color: var(--text-muted);
            font-size: 0.92rem;
            line-height: 1.6;
            margin-bottom: 1.4rem;
            flex-grow: 1;
        }

        .card-meta-row {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.25rem;
            font-size: 0.8rem;
            color: var(--text-dim);
            font-family: 'JetBrains Mono', monospace;
        }

        .card-meta-item {
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }

        .feature-bullets {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.55rem;
            margin-bottom: 1.6rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            padding-top: 1.2rem;
        }

        .bullet-item {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            font-size: 0.85rem;
            color: #cbd5e1;
        }

        .bullet-item svg {
            width: 15px;
            height: 15px;
            color: var(--accent-cyan);
            flex-shrink: 0;
        }

        .price-container {
            display: flex;
            align-items: baseline;
            margin-bottom: 1.4rem;
        }

        .price-val {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.1rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.03em;
        }

        .price-currency {
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-right: 2px;
        }

        .price-sub {
            color: var(--text-dim);
            margin-left: 0.35rem;
            font-size: 0.85rem;
        }

        .btn-card-primary {
            position: relative;
            background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
            color: #ffffff;
            border: none;
            padding: 0.9rem 1.4rem;
            font-size: 0.95rem;
            font-weight: 700;
            border-radius: var(--radius-md);
            cursor: pointer;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.55rem;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        }

        .btn-card-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(124, 58, 237, 0.5);
            background: linear-gradient(135deg, #1d4ed8 0%, #6d28d9 100%);
        }

        .btn-card-secondary {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-glass);
            color: var(--text-main);
            padding: 0.85rem 1.2rem;
            font-size: 0.9rem;
            font-weight: 600;
            border-radius: var(--radius-md);
            cursor: pointer;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            margin-top: 0.6rem;
            transition: all 0.2s ease;
        }

        .btn-card-secondary:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.2);
        }

        /* 3. Learning Platform Sandbox & Code Runner Section */
        .sandbox-section {
            background: #0b0f19;
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-lg);
            padding: 2rem;
            margin: 3rem 0;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }

        @media (max-width: 900px) {
            .sandbox-section { grid-template-columns: 1fr; }
            .cards-grid { grid-template-columns: 1fr; }
        }

        .terminal-box {
            background: #04060a;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: var(--radius-md);
            overflow: hidden;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
        }

        .terminal-header {
            background: #101626;
            padding: 0.6rem 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .terminal-dots {
            display: flex;
            gap: 6px;
        }
        .dot { width: 11px; height: 11px; border-radius: 50%; }
        .dot-red { background: #ef4444; }
        .dot-yellow { background: #f59e0b; }
        .dot-green { background: #10b981; }

        .terminal-body {
            padding: 1.25rem;
            color: #94a3b8;
            line-height: 1.6;
            min-height: 220px;
        }

        .terminal-prompt { color: #38bdf8; }
        .terminal-success { color: #86efac; }
        .terminal-warn { color: #fcd34d; }

        /* 4. Software Development Services Interactive Estimator */
        .estimator-card {
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-lg);
            padding: 2.5rem 2rem;
            margin-top: 2rem;
        }

        .estimator-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .estimator-option {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-md);
            padding: 1.25rem;
            cursor: pointer;
            transition: all 0.25s ease;
        }

        .estimator-option:hover {
            border-color: var(--accent-blue);
            background: rgba(59, 130, 246, 0.08);
        }

        .estimator-option.selected {
            border-color: var(--accent-cyan);
            background: rgba(0, 242, 254, 0.12);
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
        }

        .estimator-option h4 {
            font-size: 1rem;
            margin-bottom: 0.35rem;
        }

        .estimator-option p {
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        /* 5. Live Telemetry Dashboard View */
        .telemetry-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }

        .telemetry-stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-md);
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .stat-label {
            font-size: 0.8rem;
            color: var(--text-dim);
            font-family: 'JetBrains Mono', monospace;
            text-transform: uppercase;
        }

        .stat-value {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            color: var(--text-main);
        }

        .stat-progress {
            height: 6px;
            background: rgba(255, 255, 255, 0.06);
            border-radius: var(--radius-full);
            overflow: hidden;
        }

        .stat-progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #3b82f6, #00f2fe);
            border-radius: var(--radius-full);
            transition: width 0.5s ease;
        }

        .nodes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
            gap: 0.75rem;
            background: #04060a;
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-md);
            padding: 1.5rem;
            margin-top: 1.5rem;
        }

        .node-chip {
            background: rgba(16, 185, 129, 0.08);
            border: 1px solid rgba(16, 185, 129, 0.25);
            padding: 0.5rem;
            border-radius: var(--radius-sm);
            text-align: center;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: #86efac;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        /* Cart & Syllabus Modal */
        .cart-overlay {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(8px);
            z-index: 2000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.35s ease;
        }
        .cart-overlay.open { opacity: 1; pointer-events: auto; }

        .cart-drawer {
            position: fixed;
            top: 0;
            right: 0;
            width: 100%;
            max-width: 460px;
            height: 100vh;
            background: #0b0f19;
            border-left: 1px solid var(--border-glass);
            z-index: 2010;
            transform: translateX(100%);
            transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
            box-shadow: -10px 0 50px rgba(0, 0, 0, 0.8);
        }
        .cart-drawer.open { transform: translateX(0); }

        .drawer-header {
            padding: 1.5rem;
            border-bottom: 1px solid var(--border-glass);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .drawer-items-list {
            flex-grow: 1;
            overflow-y: auto;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .cart-item-row {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-md);
            padding: 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .drawer-footer {
            padding: 1.5rem;
            border-top: 1px solid var(--border-glass);
            background: rgba(6, 10, 20, 0.95);
        }

        .toast-container {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            z-index: 3000;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            pointer-events: none;
        }

        .toast {
            background: rgba(14, 20, 36, 0.95);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(59, 130, 246, 0.4);
            color: #fff;
            padding: 0.9rem 1.25rem;
            border-radius: var(--radius-md);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(59, 130, 246, 0.25);
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 0.9rem;
            font-weight: 600;
            min-width: 320px;
            animation: slideToast 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            pointer-events: auto;
        }

        @keyframes slideToast {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        /* Generic Modal */
        .modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(12px);
            z-index: 4000;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
            padding: 1.5rem;
        }
        .modal-overlay.open { opacity: 1; pointer-events: auto; }

        .modal-box {
            background: #0d1222;
            border: 1px solid rgba(59, 130, 246, 0.4);
            border-radius: var(--radius-lg);
            padding: 2.5rem 2rem;
            max-width: 540px;
            width: 100%;
            text-align: center;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9), 0 0 50px rgba(59, 130, 246, 0.25);
        }

        /* Footer */
        footer {
            background: #04060a;
            border-top: 1px solid var(--border-glass);
            padding: 3.5rem 1.5rem 2rem;
            color: var(--text-muted);
            font-size: 0.875rem;
        }

        .footer-grid {
            max-width: 1400px;
            margin: 0 auto 2.5rem;
            display: grid;
            grid-template-columns: 2fr repeat(3, 1fr);
            gap: 3rem;
        }

        @media (max-width: 768px) {
            .footer-grid { grid-template-columns: 1fr; gap: 2rem; }
            .navbar { flex-wrap: wrap; gap: 1rem; }
            .nav-links { overflow-x: auto; width: 100%; padding-bottom: 0.5rem; }
        }

        .footer-col h5 {
            color: var(--text-main);
            font-size: 0.95rem;
            margin-bottom: 1rem;
            font-family: 'Space Grotesk', sans-serif;
        }

        .footer-col ul { list-style: none; display: flex; flex-direction: column; gap: 0.6rem; }
        .footer-col a { color: var(--text-dim); text-decoration: none; transition: color 0.2s; }
        .footer-col a:hover { color: var(--accent-cyan); }
    </style>
</head>
<body>
    <div class="bg-canvas"></div>
    <div class="grid-overlay"></div>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>

    <!-- 1. Top Live Status Bar -->
    <div class="status-bar-wrapper">
        <div class="status-bar">
            <div class="status-left">
                <div class="pulse-beacon"></div>
                <span>🟢 Server Status: 100% Healthy | AIOps Store</span>
            </div>
            <div class="status-metrics">
                <div class="metric-pill"><span>UPTIME</span><span class="val">99.999%</span></div>
                <div class="metric-pill"><span>LATENCY</span><span class="val" id="telemetry-latency">11ms</span></div>
                <div class="metric-pill"><span>K8S PODS</span><span class="val">128 RUNNING</span></div>
            </div>
        </div>
    </div>

    <!-- 2. Main Navigation Bar -->
    <div class="navbar-wrapper">
        <nav class="navbar">
            <div class="brand-logo" onclick="switchView('store')">
                <div class="brand-icon">⚡</div>
                <div>
                    <span>AIOps Tech & Academy</span>
                    <span class="brand-badge">ENTERPRISE</span>
                </div>
            </div>

            <ul class="nav-links">
                <li><a class="nav-item active" id="nav-store" onclick="switchView('store')"><i data-lucide="layout-grid"></i> Tech Store</a></li>
                <li><a class="nav-item" id="nav-academy" onclick="switchView('academy')"><i data-lucide="graduation-cap"></i> Learning Academy</a></li>
                <li><a class="nav-item" id="nav-services" onclick="switchView('services')"><i data-lucide="code-2"></i> Software Dev & Services</a></li>
                <li><a class="nav-item" id="nav-telemetry" onclick="switchView('telemetry')"><i data-lucide="activity"></i> Cluster Telemetry</a></li>
                <li><a class="nav-item" id="nav-about" onclick="switchView('about')"><i data-lucide="shield-check"></i> Enterprise SLA</a></li>
            </ul>

            <div class="nav-actions">
                <button class="cart-trigger-btn" onclick="toggleCartDrawer()">
                    <i data-lucide="shopping-cart"></i>
                    <span>Cart / Enrolled</span>
                    <span class="cart-count-badge" id="cart-badge">0</span>
                </button>
            </div>
        </nav>
    </div>

    <!-- ================= VIEW 1: TECH STORE & PRODUCTS ================= -->
    <section class="view-container active" id="view-store">
        <header class="hero">
            <div class="hero-badge">
                <i data-lucide="sparkles"></i>
                <span>Next-Gen Enterprise Infrastructure & Software Solutions</span>
            </div>
            <h1>🚀 AIOps Tech Store</h1>
            <p class="subtitle">Microservices Architecture System</p>
        </header>

        <!-- Search & Category Filters -->
        <div class="search-filter-wrapper">
            <div class="search-box">
                <i data-lucide="search" style="color: var(--text-dim); width: 18px;"></i>
                <input type="text" id="store-search" placeholder="Search compute, AI agents, security..." oninput="filterStoreProducts()">
            </div>
            <div class="filters-group">
                <button class="filter-btn active" onclick="setStoreCategory('all', this)">All Solutions</button>
                <button class="filter-btn" onclick="setStoreCategory('compute', this)">Compute & Servers</button>
                <button class="filter-btn" onclick="setStoreCategory('ai', this)">AI Agents</button>
                <button class="filter-btn" onclick="setStoreCategory('security', this)">Cyber Security</button>
                <button class="filter-btn" onclick="setStoreCategory('enterprise', this)">Enterprise DevOps</button>
            </div>
        </div>

        <div class="cards-grid" id="store-cards-grid">
            <!-- Product 1: Cloud Server Pro (Required) -->
            <div class="premium-card" data-cat="compute" data-name="Cloud Server Pro">
                <div>
                    <div class="card-header-top">
                        <div class="card-icon-box" style="background: rgba(59, 130, 246, 0.15); border-color: rgba(59, 130, 246, 0.3);">☁️</div>
                        <span class="card-badge badge-cyan">High Compute</span>
                    </div>
                    <h3 class="card-title">Cloud Server Pro</h3>
                    <p class="card-desc">High-performance scalable cloud compute instance optimized for resilient microservices workloads and automated Kubernetes clustering.</p>
                    <ul class="feature-bullets">
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> 64 vCPU | 256GB ECC RAM Tier</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> 4TB NVMe Gen4 Array with Auto-Backup</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> 99.999% SLA Uptime Guarantee</li>
                    </ul>
                </div>
                <div>
                    <div class="price-container">
                        <span class="price-currency">$</span>
                        <span class="price-val">99.99</span>
                        <span class="price-sub">/month</span>
                    </div>
                    <button class="btn-card-primary" onclick="addToCart('Cloud Server Pro', 99.99, '☁️', 'Infrastructure')">
                        <i data-lucide="shopping-bag"></i> Add to Cart
                    </button>
                </div>
            </div>

            <!-- Product 2: AI Assistant Bot (Required) -->
            <div class="premium-card" data-cat="ai" data-name="AI Assistant Bot">
                <div>
                    <div class="card-header-top">
                        <div class="card-icon-box" style="background: rgba(139, 92, 246, 0.15); border-color: rgba(139, 92, 246, 0.3);">🤖</div>
                        <span class="card-badge badge-pink">AI Agent</span>
                    </div>
                    <h3 class="card-title">AI Assistant Bot</h3>
                    <p class="card-desc">Autonomous AIOps operational assistant for real-time log telemetry analysis, automated root-cause detection, and self-healing cluster recovery.</p>
                    <ul class="feature-bullets">
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Autonomous Incident Remediation Agent</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Real-time Telemetry Anomaly Predictor</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Multi-channel Slack & PagerDuty Integration</li>
                    </ul>
                </div>
                <div>
                    <div class="price-container">
                        <span class="price-currency">$</span>
                        <span class="price-val">49.99</span>
                        <span class="price-sub">/month</span>
                    </div>
                    <button class="btn-card-primary" onclick="addToCart('AI Assistant Bot', 49.99, '🤖', 'AI Ops')">
                        <i data-lucide="shopping-bag"></i> Add to Cart
                    </button>
                </div>
            </div>

            <!-- Product 3: Security Firewall (Required) -->
            <div class="premium-card" data-cat="security" data-name="Security Firewall">
                <div>
                    <div class="card-header-top">
                        <div class="card-icon-box" style="background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.3);">🛡️</div>
                        <span class="card-badge badge-green">Zero Trust</span>
                    </div>
                    <h3 class="card-title">Security Firewall</h3>
                    <p class="card-desc">Next-gen zero-trust application gateway firewall with deep packet inspection, multi-terabit DDoS mitigation, and vulnerability scanning.</p>
                    <ul class="feature-bullets">
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Layer 7 Intelligent WAF & API Defense</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Automated TLS 1.3 & mTLS Enforcement</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Continuous OWASP Top 10 Threat Shield</li>
                    </ul>
                </div>
                <div>
                    <div class="price-container">
                        <span class="price-currency">$</span>
                        <span class="price-val">29.99</span>
                        <span class="price-sub">/month</span>
                    </div>
                    <button class="btn-card-primary" onclick="addToCart('Security Firewall', 29.99, '🛡️', 'CyberSecurity')">
                        <i data-lucide="shopping-bag"></i> Add to Cart
                    </button>
                </div>
            </div>

            <!-- Product 4: Enterprise DevOps Suite -->
            <div class="premium-card" data-cat="enterprise" data-name="DevOps Enterprise Suite">
                <div>
                    <div class="card-header-top">
                        <div class="card-icon-box" style="background: rgba(245, 158, 11, 0.15); border-color: rgba(245, 158, 11, 0.3);">⚡</div>
                        <span class="card-badge badge-amber">CI/CD Engine</span>
                    </div>
                    <h3 class="card-title">DevOps Enterprise Suite</h3>
                    <p class="card-desc">Complete end-to-end GitOps pipeline engine with automated canary deployments, Helm chart synchronization, and multi-cloud telemetry.</p>
                    <ul class="feature-bullets">
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Zero-Downtime Blue/Green Rollouts</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Automated Container Image CVE Scanner</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Terraform & OpenTofu State Manager</li>
                    </ul>
                </div>
                <div>
                    <div class="price-container">
                        <span class="price-currency">$</span>
                        <span class="price-val">149.99</span>
                        <span class="price-sub">/month</span>
                    </div>
                    <button class="btn-card-primary" onclick="addToCart('DevOps Enterprise Suite', 149.99, '⚡', 'Enterprise')">
                        <i data-lucide="shopping-bag"></i> Add to Cart
                    </button>
                </div>
            </div>

            <!-- Product 5: LLM Ops Pipeline Engine -->
            <div class="premium-card" data-cat="ai" data-name="LLM Ops Pipeline Engine">
                <div>
                    <div class="card-header-top">
                        <div class="card-icon-box" style="background: rgba(236, 72, 153, 0.15); border-color: rgba(236, 72, 153, 0.3);">🧠</div>
                        <span class="card-badge badge-pink">Generative AI</span>
                    </div>
                    <h3 class="card-title">LLM Ops Pipeline Engine</h3>
                    <p class="card-desc">Managed vector database and RAG microservice layer for fine-tuning, evaluating, and serving enterprise large language models securely.</p>
                    <ul class="feature-bullets">
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> High-Throughput vLLM & TensorRT Inference</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Hybrid Vector Indexing & Semantic Cache</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Prompt Injection Guardrails</li>
                    </ul>
                </div>
                <div>
                    <div class="price-container">
                        <span class="price-currency">$</span>
                        <span class="price-val">199.99</span>
                        <span class="price-sub">/month</span>
                    </div>
                    <button class="btn-card-primary" onclick="addToCart('LLM Ops Pipeline Engine', 199.99, '🧠', 'AI Ops')">
                        <i data-lucide="shopping-bag"></i> Add to Cart
                    </button>
                </div>
            </div>

            <!-- Product 6: Microservices API Gateway -->
            <div class="premium-card" data-cat="compute" data-name="Microservices API Gateway">
                <div>
                    <div class="card-header-top">
                        <div class="card-icon-box" style="background: rgba(0, 242, 254, 0.15); border-color: rgba(0, 242, 254, 0.3);">🌐</div>
                        <span class="card-badge badge-cyan">Low Latency</span>
                    </div>
                    <h3 class="card-title">Microservices API Gateway</h3>
                    <p class="card-desc">Sub-millisecond dynamic routing gateway supporting gRPC, REST, GraphQL, rate limiting, and distributed OpenTelemetry tracing.</p>
                    <ul class="feature-bullets">
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> 1,000,000+ Req/sec per instance</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> OAuth2 / JWT Auth Token Verification</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Automatic Service Discovery & Circuit Breaker</li>
                    </ul>
                </div>
                <div>
                    <div class="price-container">
                        <span class="price-currency">$</span>
                        <span class="price-val">79.99</span>
                        <span class="price-sub">/month</span>
                    </div>
                    <button class="btn-card-primary" onclick="addToCart('Microservices API Gateway', 79.99, '🌐', 'Networking')">
                        <i data-lucide="shopping-bag"></i> Add to Cart
                    </button>
                </div>
            </div>
        </div>
    </section>

    <!-- ================= VIEW 2: LEARNING PLATFORM & ACADEMY ================= -->
    <section class="view-container" id="view-academy">
        <header class="hero">
            <div class="hero-badge">
                <i data-lucide="award"></i>
                <span>Industry-Recognized DevOps, AI & Cloud Engineering Tracks</span>
            </div>
            <h1>🎓 AIOps Learning Academy</h1>
            <p class="subtitle">Master real-world microservices, Kubernetes orchestration, autonomous AI agents, and production DevOps through hands-on cloud labs.</p>
        </header>

        <div class="cards-grid">
            <!-- Course 1 -->
            <div class="premium-card">
                <div>
                    <div class="card-header-top">
                        <div class="card-icon-box" style="background: rgba(59, 130, 246, 0.15); border-color: rgba(59, 130, 246, 0.3);">🚀</div>
                        <span class="card-badge badge-cyan">12 Weeks • Professional</span>
                    </div>
                    <h3 class="card-title">Certified AIOps & Cloud Architect</h3>
                    <p class="card-desc">Complete curriculum covering distributed systems resilience, automated root cause analysis, Prometheus/Grafana alerting, and Chaos Engineering.</p>
                    <div class="card-meta-row">
                        <div class="card-meta-item"><i data-lucide="clock" style="width: 14px;"></i> 48 Hours Live</div>
                        <div class="card-meta-item"><i data-lucide="layers" style="width: 14px;"></i> 24 Cloud Labs</div>
                    </div>
                    <ul class="feature-bullets">
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Hands-on Kubernetes Chaos Mesh Experiments</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Machine Learning for Anomaly Detection</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Industry Certification & Portfolio Capstone</li>
                    </ul>
                </div>
                <div>
                    <div class="price-container">
                        <span class="price-currency">$</span>
                        <span class="price-val">249.00</span>
                        <span class="price-sub">one-time</span>
                    </div>
                    <button class="btn-card-primary" onclick="addToCart('Course: Certified AIOps Architect', 249.00, '🚀', 'Academy')">
                        <i data-lucide="graduation-cap"></i> Enroll Now
                    </button>
                    <button class="btn-card-secondary" onclick="viewSyllabus('Certified AIOps Architect', '12 Weeks: Cloud Native architecture, Chaos Engineering, ML telemetry analysis, OpenTelemetry & K8s operators.')">
                        <i data-lucide="book-open"></i> View Syllabus
                    </button>
                </div>
            </div>

            <!-- Course 2 -->
            <div class="premium-card">
                <div>
                    <div class="card-header-top">
                        <div class="card-icon-box" style="background: rgba(139, 92, 246, 0.15); border-color: rgba(139, 92, 246, 0.3);">🧠</div>
                        <span class="card-badge badge-purple">10 Weeks • Advanced</span>
                    </div>
                    <h3 class="card-title">Generative AI & Agent Engineering</h3>
                    <p class="card-desc">Architect autonomous multi-agent swarms, tool-use execution graphs, LangGraph architectures, and high-performance RAG vector pipelines.</p>
                    <div class="card-meta-row">
                        <div class="card-meta-item"><i data-lucide="clock" style="width: 14px;"></i> 40 Hours Live</div>
                        <div class="card-meta-item"><i data-lucide="layers" style="width: 14px;"></i> 18 Projects</div>
                    </div>
                    <ul class="feature-bullets">
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Build Self-Correcting Python AI Agents</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Multi-Agent Orchestration & Memory Systems</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Fine-tuning Open-Source Models on GPUs</li>
                    </ul>
                </div>
                <div>
                    <div class="price-container">
                        <span class="price-currency">$</span>
                        <span class="price-val">299.00</span>
                        <span class="price-sub">one-time</span>
                    </div>
                    <button class="btn-card-primary" onclick="addToCart('Course: Generative AI & Agent Eng', 299.00, '🧠', 'Academy')">
                        <i data-lucide="graduation-cap"></i> Enroll Now
                    </button>
                    <button class="btn-card-secondary" onclick="viewSyllabus('Generative AI & Agent Engineering', '10 Weeks: Tool-use paradigms, LangGraph state machines, vector embeddings, fine-tuning, latency optimization.')">
                        <i data-lucide="book-open"></i> View Syllabus
                    </button>
                </div>
            </div>

            <!-- Course 3 -->
            <div class="premium-card">
                <div>
                    <div class="card-header-top">
                        <div class="card-icon-box" style="background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.3);">🛡️</div>
                        <span class="card-badge badge-green">8 Weeks • Intensive</span>
                    </div>
                    <h3 class="card-title">Production Kubernetes & DevSecOps</h3>
                    <p class="card-desc">Zero-trust security policies, Istio Service Mesh, eBPF network observability with Cilium, and GitOps automated vulnerability scanning.</p>
                    <div class="card-meta-row">
                        <div class="card-meta-item"><i data-lucide="clock" style="width: 14px;"></i> 32 Hours Live</div>
                        <div class="card-meta-item"><i data-lucide="layers" style="width: 14px;"></i> 15 Sandboxes</div>
                    </div>
                    <ul class="feature-bullets">
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Istio mTLS & eBPF Security Observability</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> ArgoCD GitOps Continuous Delivery</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> CKS (Certified K8s Security) Prep</li>
                    </ul>
                </div>
                <div>
                    <div class="price-container">
                        <span class="price-currency">$</span>
                        <span class="price-val">199.00</span>
                        <span class="price-sub">one-time</span>
                    </div>
                    <button class="btn-card-primary" onclick="addToCart('Course: Kubernetes & DevSecOps', 199.00, '🛡️', 'Academy')">
                        <i data-lucide="graduation-cap"></i> Enroll Now
                    </button>
                    <button class="btn-card-secondary" onclick="viewSyllabus('Production Kubernetes & DevSecOps', '8 Weeks: Container hardening, RBAC, Network policies, Cilium eBPF, ArgoCD pipelines, Secret vaults.')">
                        <i data-lucide="book-open"></i> View Syllabus
                    </button>
                </div>
            </div>
        </div>

        <!-- Interactive Hands-on Cloud Sandbox Demo -->
        <div class="sandbox-section">
            <div>
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.6rem; margin-bottom: 0.75rem;">⚡ Interactive Cloud Lab Sandbox</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem;">
                    Test commands right from your browser. Our learning platform spins up ephemeral isolated Kubernetes clusters in under 500ms for every student.
                </p>
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.5rem;">
                    <button class="filter-btn active" onclick="runSandboxCmd('kubectl get pods -A')">kubectl get pods</button>
                    <button class="filter-btn" onclick="runSandboxCmd('aiops diagnose --cluster prod-us-east')">aiops diagnose</button>
                    <button class="filter-btn" onclick="runSandboxCmd('helm upgrade --install microservices ./chart')">helm deploy</button>
                </div>
                <div style="color: var(--accent-cyan); font-size: 0.85rem; font-weight: 600;">
                    ✓ Zero installation required &bull; Real terminal output
                </div>
            </div>

            <div class="terminal-box">
                <div class="terminal-header">
                    <div class="terminal-dots">
                        <div class="dot dot-red"></div>
                        <div class="dot dot-yellow"></div>
                        <div class="dot dot-green"></div>
                    </div>
                    <span style="color: var(--text-dim); font-size: 0.75rem;">student@aiops-sandbox-lab:~</span>
                    <i data-lucide="terminal" style="width: 14px; color: var(--text-dim);"></i>
                </div>
                <div class="terminal-body" id="sandbox-output">
                    <span class="terminal-prompt">$ kubectl get pods -n aiops-system</span><br>
                    NAME                                READY   STATUS    RESTARTS   AGE<br>
                    aiops-telemetry-collector-7d8b89    1/1     <span class="terminal-success">Running</span>   0          42m<br>
                    aiops-anomaly-agent-68df84c4f-2kq   1/1     <span class="terminal-success">Running</span>   0          42m<br>
                    gateway-ingress-envoy-5c94bb9-xpl   1/1     <span class="terminal-success">Running</span>   0          42m<br>
                    <br>
                    <span class="terminal-prompt">$ aiops-agent --health-check</span><br>
                    <span class="terminal-success">[SUCCESS]</span> Cluster health score: 100%. All 24 node groups synchronized.
                </div>
            </div>
        </div>
    </section>

    <!-- ================= VIEW 3: SOFTWARE DEV & ENTERPRISE SERVICES ================= -->
    <section class="view-container" id="view-services">
        <header class="hero">
            <div class="hero-badge">
                <i data-lucide="code-2"></i>
                <span>Custom Software Engineering & Cloud Modernization</span>
            </div>
            <h1>🛠️ Enterprise Software Development</h1>
            <p class="subtitle">We build resilient distributed systems, custom AI agent workflows, modern web platforms, and automated cloud infrastructure for high-growth enterprises.</p>
        </header>

        <div class="cards-grid">
            <div class="premium-card">
                <div>
                    <div class="card-header-top">
                        <div class="card-icon-box" style="background: rgba(59, 130, 246, 0.15);">🏢</div>
                        <span class="card-badge badge-cyan">Full-Cycle Dev</span>
                    </div>
                    <h3 class="card-title">Microservices Modernization</h3>
                    <p class="card-desc">Deconstruct legacy monoliths into lightweight, event-driven microservices architecture using Go, Python, and Kafka.</p>
                    <ul class="feature-bullets">
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Domain-Driven Design (DDD) & Event Sourcing</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> 10x Throughput & Sub-10ms Latency Tuning</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Zero Downtime Migration Strategy</li>
                    </ul>
                </div>
                <button class="btn-card-primary" onclick="requestQuote('Microservices Modernization')">
                    <i data-lucide="send"></i> Request Engineering Quote
                </button>
            </div>

            <div class="premium-card">
                <div>
                    <div class="card-header-top">
                        <div class="card-icon-box" style="background: rgba(139, 92, 246, 0.15);">🤖</div>
                        <span class="card-badge badge-purple">AI Workflows</span>
                    </div>
                    <h3 class="card-title">Custom AI Agent Integration</h3>
                    <p class="card-desc">Develop bespoke autonomous agents that interface directly with your ERP, CRM, and databases to automate complex business workflows.</p>
                    <ul class="feature-bullets">
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Private On-Premise LLM Deployments</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Secure RBAC Data Ingestion Pipelines</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Automated Multi-Step Reasoning Engine</li>
                    </ul>
                </div>
                <button class="btn-card-primary" onclick="requestQuote('Custom AI Agent Integration')">
                    <i data-lucide="send"></i> Request Engineering Quote
                </button>
            </div>

            <div class="premium-card">
                <div>
                    <div class="card-header-top">
                        <div class="card-icon-box" style="background: rgba(16, 185, 129, 0.15);">☁️</div>
                        <span class="card-badge badge-green">Cloud & GitOps</span>
                    </div>
                    <h3 class="card-title">Infrastructure as Code & CI/CD</h3>
                    <p class="card-desc">End-to-end multi-region infrastructure provisioning using Terraform, Kubernetes, ArgoCD, and automated security guardrails.</p>
                    <ul class="feature-bullets">
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> Multi-Cloud AWS / GCP / Azure Architecture</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> SOC2 & ISO27001 Compliance Automation</li>
                        <li class="bullet-item"><i data-lucide="check-circle-2"></i> 24/7 Dedicated Site Reliability Engineering</li>
                    </ul>
                </div>
                <button class="btn-card-primary" onclick="requestQuote('Infrastructure as Code & CI/CD')">
                    <i data-lucide="send"></i> Request Engineering Quote
                </button>
            </div>
        </div>

        <!-- Interactive Project Estimator -->
        <div class="estimator-card">
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.6rem; margin-bottom: 0.5rem;">📊 Interactive Project Cost & Timeline Estimator</h3>
            <p style="color: var(--text-muted); font-size: 0.95rem;">Select your architectural requirements to generate an instant ballpark estimate.</p>

            <div class="estimator-grid">
                <div class="estimator-option selected" onclick="toggleEstimatorOption(this, 3000, 2)">
                    <h4>☁️ Cloud Microservices</h4>
                    <p>Distributed Docker/K8s Architecture</p>
                </div>
                <div class="estimator-option selected" onclick="toggleEstimatorOption(this, 4500, 3)">
                    <h4>🤖 Custom AI Agents</h4>
                    <p>Multi-Agent Reasoning & RAG</p>
                </div>
                <div class="estimator-option" onclick="toggleEstimatorOption(this, 2500, 2)">
                    <h4>🛡️ DevSecOps & WAF</h4>
                    <p>Zero-Trust Security & CI/CD</p>
                </div>
                <div class="estimator-option" onclick="toggleEstimatorOption(this, 3500, 3)">
                    <h4>⚡ High-Speed API Gateway</h4>
                    <p>Sub-ms gRPC & REST Routing</p>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.4); padding: 1.5rem; border-radius: var(--radius-md); border: 1px solid var(--border-glass);">
                <div>
                    <div style="font-size: 0.85rem; color: var(--text-dim); text-transform: uppercase; font-family: 'JetBrains Mono';">Estimated Timeline & Budget</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: var(--accent-cyan); font-family: 'Space Grotesk';" id="estimator-total">$7,500 &bull; ~5 Weeks Delivery</div>
                </div>
                <button class="btn-card-primary" style="width: auto; padding: 0.85rem 2rem;" onclick="openEstimateModal()">
                    <i data-lucide="check-circle"></i> Book Discovery Call
                </button>
            </div>
        </div>
    </section>

    <!-- ================= VIEW 4: LIVE TELEMETRY ================= -->
    <section class="view-container" id="view-telemetry">
        <header class="hero">
            <div class="hero-badge">
                <i data-lucide="activity"></i>
                <span>Real-Time Production Cluster Telemetry</span>
            </div>
            <h1>📊 AIOps Live Infrastructure Monitor</h1>
            <p class="subtitle">Global distributed nodes, latency metrics, and real-time self-healing cluster diagnostics.</p>
        </header>

        <div class="telemetry-grid">
            <div class="telemetry-stat-card">
                <div class="stat-label">Global CPU Load</div>
                <div class="stat-value" id="stat-cpu">14.2%</div>
                <div class="stat-progress"><div class="stat-progress-bar" id="bar-cpu" style="width: 14.2%;"></div></div>
            </div>
            <div class="telemetry-stat-card">
                <div class="stat-label">RAM Utilization</div>
                <div class="stat-value" id="stat-ram">38.7%</div>
                <div class="stat-progress"><div class="stat-progress-bar" id="bar-ram" style="width: 38.7%; background: linear-gradient(90deg, #8b5cf6, #ec4899);"></div></div>
            </div>
            <div class="telemetry-stat-card">
                <div class="stat-label">Network Throughput</div>
                <div class="stat-value" id="stat-net">4.82 Gbps</div>
                <div class="stat-progress"><div class="stat-progress-bar" id="bar-net" style="width: 65%; background: linear-gradient(90deg, #10b981, #00f2fe);"></div></div>
            </div>
            <div class="telemetry-stat-card">
                <div class="stat-label">Error Rate</div>
                <div class="stat-value" style="color: #86efac;">0.0001%</div>
                <div class="stat-progress"><div class="stat-progress-bar" style="width: 1%; background: #10b981;"></div></div>
            </div>
        </div>

        <div class="estimator-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="font-family: 'Space Grotesk'; font-size: 1.4rem;">🌐 Active Kubernetes Node Topology (24 Nodes Online)</h3>
                <span style="color: #86efac; font-size: 0.85rem; font-family: 'JetBrains Mono';">● 100% HEALTHY</span>
            </div>
            <div class="nodes-grid" id="nodes-container">
                <!-- Injected via JS -->
            </div>
        </div>
    </section>

    <!-- ================= VIEW 5: ENTERPRISE SLA & ABOUT ================= -->
    <section class="view-container" id="view-about">
        <header class="hero">
            <div class="hero-badge">
                <i data-lucide="shield"></i>
                <span>Enterprise Service Level Agreements</span>
            </div>
            <h1>🏢 Why Global Teams Choose AIOps</h1>
            <p class="subtitle">Trusted by fast-moving startups and Fortune 500 enterprises for mission-critical microservices development and elite engineering training.</p>
        </header>

        <div class="cards-grid">
            <div class="premium-card">
                <div class="card-icon-box" style="background: rgba(16, 185, 129, 0.15); margin-bottom: 1.25rem;">🔒</div>
                <h3 class="card-title">99.999% SLA Guaranteed</h3>
                <p class="card-desc">Our multi-region active-active clusters with automated sub-second failover ensure your applications remain online through any cloud outage.</p>
            </div>
            <div class="premium-card">
                <div class="card-icon-box" style="background: rgba(59, 130, 246, 0.15); margin-bottom: 1.25rem;">⚡</div>
                <h3 class="card-title">Autonomous AI Healing</h3>
                <p class="card-desc">Machine learning agents resolve 85% of infrastructure alerts and memory leaks before they ever impact production traffic or trigger a pager.</p>
            </div>
            <div class="premium-card">
                <div class="card-icon-box" style="background: rgba(139, 92, 246, 0.15); margin-bottom: 1.25rem;">🎓</div>
                <h3 class="card-title">Elite Training & Mentorship</h3>
                <p class="card-desc">Every enterprise development contract includes dedicated engineering workshops and certified academy tracks for your internal developers.</p>
            </div>
        </div>
    </section>

    <!-- Interactive Cart / Enrollment Slide-Over Drawer -->
    <div class="cart-overlay" id="cart-overlay" onclick="toggleCartDrawer()"></div>
    <aside class="cart-drawer" id="cart-drawer">
        <div class="drawer-header">
            <h3 style="font-family: 'Space Grotesk'; font-size: 1.3rem; display: flex; align-items: center; gap: 0.5rem;">
                <i data-lucide="shopping-cart"></i> Cart & Enrollments
            </h3>
            <button class="filter-btn" onclick="toggleCartDrawer()"><i data-lucide="x"></i></button>
        </div>
        <div class="drawer-items-list" id="cart-items-container">
            <!-- Dynamic Items -->
        </div>
        <div class="drawer-footer">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
                <span style="font-weight: 600; color: var(--text-muted);">Total Amount:</span>
                <span style="font-family: 'Space Grotesk'; font-size: 1.6rem; font-weight: 800; color: var(--accent-cyan);" id="cart-total-display">$0.00</span>
            </div>
            <button class="btn-card-primary" style="background: linear-gradient(135deg, #10b981, #059669);" onclick="openCheckoutModal()">
                <i data-lucide="check"></i> Complete Checkout & Deploy
            </button>
        </div>
    </aside>

    <!-- Checkout / Quote Modal -->
    <div class="modal-overlay" id="checkout-modal">
        <div class="modal-box">
            <div style="width: 68px; height: 68px; background: rgba(16, 185, 129, 0.15); border: 2px solid var(--accent-green); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; color: var(--accent-green);">
                <i data-lucide="check-check" style="width: 36px; height: 36px;"></i>
            </div>
            <h2 style="font-family: 'Space Grotesk'; font-size: 1.85rem; margin-bottom: 0.75rem;" id="modal-title">Order Provisioned! 🚀</h2>
            <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin-bottom: 2rem;" id="modal-desc">
                Your software license keys and learning academy tokens have been deployed. Credentials have been sent to your primary developer account.
            </p>
            <button class="btn-card-primary" onclick="closeCheckoutModal()">
                Return to Dashboard
            </button>
        </div>
    </div>

    <!-- Toast Notifications Container -->
    <div class="toast-container" id="toast-container"></div>

    <!-- Footer -->
    <footer>
        <div class="footer-grid">
            <div>
                <div class="brand-logo" style="margin-bottom: 1rem;">
                    <div class="brand-icon">⚡</div>
                    <span>AIOps Tech & Academy</span>
                </div>
                <p style="color: var(--text-dim); line-height: 1.6; max-width: 340px;">
                    Empowering global engineering teams with high-availability microservices architecture, autonomous AI agents, and production cloud learning.
                </p>
            </div>
            <div class="footer-col">
                <h5>Tech Solutions</h5>
                <ul>
                    <li><a href="#" onclick="switchView('store')">Cloud Server Pro</a></li>
                    <li><a href="#" onclick="switchView('store')">AI Assistant Bot</a></li>
                    <li><a href="#" onclick="switchView('store')">Security Firewall</a></li>
                    <li><a href="#" onclick="switchView('store')">DevOps Suite</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h5>Learning Academy</h5>
                <ul>
                    <li><a href="#" onclick="switchView('academy')">AIOps Architect</a></li>
                    <li><a href="#" onclick="switchView('academy')">Generative AI Agents</a></li>
                    <li><a href="#" onclick="switchView('academy')">Kubernetes DevSecOps</a></li>
                    <li><a href="#" onclick="switchView('academy')">Certifications</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h5>Software Dev</h5>
                <ul>
                    <li><a href="#" onclick="switchView('services')">Microservices Migration</a></li>
                    <li><a href="#" onclick="switchView('services')">Custom AI Integrations</a></li>
                    <li><a href="#" onclick="switchView('services')">Infrastructure as Code</a></li>
                    <li><a href="#" onclick="switchView('telemetry')">Live Telemetry</a></li>
                </ul>
            </div>
        </div>
        <div style="text-align: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 1.5rem; color: var(--text-dim);">
            &copy; 2026 AIOps Software Development & Learning Platform &bull; All Rights Reserved &bull; Microservices Architecture System
        </div>
    </footer>

    <!-- Interactive Scripts -->
    <script>
        lucide.createIcons();

        // 1. Navigation SPA View Switcher
        function switchView(viewName) {
            document.querySelectorAll('.view-container').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            
            const targetView = document.getElementById('view-' + viewName);
            const targetNav = document.getElementById('nav-' + viewName);
            
            if (targetView) targetView.classList.add('active');
            if (targetNav) targetNav.classList.add('active');

            window.scrollTo({ top: 0, behavior: 'smooth' });
            lucide.createIcons();
        }

        // 2. Shopping Cart & Enrollment State
        let cart = [];

        function addToCart(title, price, emoji, category) {
            cart.push({ id: Date.now() + Math.random(), title, price, emoji, category });
            updateCartUI();
            showToast(`Added <strong>${title}</strong> ($${price.toFixed(2)})!`);

            const badge = document.getElementById('cart-badge');
            badge.classList.remove('cart-bump');
            void badge.offsetWidth;
            badge.classList.add('cart-bump');

            confetti({
                particleCount: 25,
                spread: 45,
                origin: { y: 0.8 },
                colors: ['#00f2fe', '#3b82f6', '#8b5cf6', '#10b981']
            });
        }

        function removeFromCart(id) {
            cart = cart.filter(i => i.id !== id);
            updateCartUI();
        }

        function updateCartUI() {
            const badge = document.getElementById('cart-badge');
            const container = document.getElementById('cart-items-container');
            const totalDisplay = document.getElementById('cart-total-display');

            badge.textContent = cart.length;

            if (cart.length === 0) {
                container.innerHTML = `
                    <div style="text-align: center; color: var(--text-muted); padding: 3rem 1rem;">
                        <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.4;">🛒</div>
                        <p style="font-weight: 600;">Your cart and enrollments are empty.</p>
                        <span style="font-size: 0.8rem; color: var(--text-dim);">Select software products or courses to get started.</span>
                    </div>
                `;
                totalDisplay.textContent = '$0.00';
                return;
            }

            let total = 0;
            container.innerHTML = cart.map(item => {
                total += item.price;
                return `
                    <div class="cart-item-row">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <div style="font-size: 1.5rem; width: 40px; height: 40px; background: rgba(255,255,255,0.05); border-radius: 8px; display: flex; align-items: center; justify-content: center;">${item.emoji}</div>
                            <div>
                                <div style="font-size: 0.9rem; font-weight: 700;">${item.title}</div>
                                <div style="font-size: 0.8rem; color: var(--accent-cyan);">$${item.price.toFixed(2)}</div>
                            </div>
                        </div>
                        <button class="filter-btn" style="padding: 0.35rem 0.6rem; color: #ef4444;" onclick="removeFromCart(${item.id})">
                            <i data-lucide="trash-2" style="width: 14px; height: 14px;"></i>
                        </button>
                    </div>
                `;
            }).join('');

            totalDisplay.textContent = '$' + total.toFixed(2);
            lucide.createIcons();
        }

        function toggleCartDrawer() {
            document.getElementById('cart-overlay').classList.toggle('open');
            document.getElementById('cart-drawer').classList.toggle('open');
        }

        function openCheckoutModal() {
            if (cart.length === 0) {
                showToast("Your cart is empty! Select products or courses first.");
                return;
            }
            toggleCartDrawer();
            document.getElementById('modal-title').textContent = "Order & Enrollment Complete! 🚀";
            document.getElementById('modal-desc').textContent = "Your microservices subscriptions and academy course credentials have been successfully activated.";
            document.getElementById('checkout-modal').classList.add('open');

            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.6 },
                colors: ['#00f2fe', '#3b82f6', '#8b5cf6', '#ec4899', '#10b981']
            });
        }

        function closeCheckoutModal() {
            document.getElementById('checkout-modal').classList.remove('open');
            cart = [];
            updateCartUI();
        }

        // 3. Toast System
        function showToast(msg) {
            const c = document.getElementById('toast-container');
            const t = document.createElement('div');
            t.className = 'toast';
            t.innerHTML = `<i data-lucide="check-circle" style="color: var(--accent-green); width: 18px; flex-shrink: 0;"></i> <div>${msg}</div>`;
            c.appendChild(t);
            lucide.createIcons();
            setTimeout(() => {
                t.style.opacity = '0';
                t.style.transform = 'translateY(15px)';
                t.style.transition = 'all 0.3s ease';
                setTimeout(() => t.remove(), 300);
            }, 3000);
        }

        // 4. Store Filters & Search
        let currentStoreCat = 'all';
        function setStoreCategory(cat, btn) {
            document.querySelectorAll('#view-store .filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentStoreCat = cat;
            filterStoreProducts();
        }

        function filterStoreProducts() {
            const query = (document.getElementById('store-search').value || '').toLowerCase();
            const cards = document.querySelectorAll('#store-cards-grid .premium-card');
            cards.forEach(card => {
                const name = (card.getAttribute('data-name') || '').toLowerCase();
                const cat = card.getAttribute('data-cat') || '';
                const matchCat = (currentStoreCat === 'all' || cat === currentStoreCat);
                const matchQuery = name.includes(query);
                if (matchCat && matchQuery) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        // 5. Interactive Sandbox Terminal
        function runSandboxCmd(cmd) {
            const out = document.getElementById('sandbox-output');
            let res = '';
            if (cmd.includes('get pods')) {
                res = `<span class="terminal-prompt">$ ${cmd}</span><br>NAME                                READY   STATUS    RESTARTS   AGE<br>aiops-telemetry-collector-7d8b89    1/1     <span class="terminal-success">Running</span>   0          48m<br>aiops-anomaly-agent-68df84c4f-2kq   1/1     <span class="terminal-success">Running</span>   0          48m<br>gateway-ingress-envoy-5c94bb9-xpl   1/1     <span class="terminal-success">Running</span>   0          48m`;
            } else if (cmd.includes('diagnose')) {
                res = `<span class="terminal-prompt">$ ${cmd}</span><br>[AI-DIAGNOSE] Querying 1,450 telemetry metric streams...<br><span class="terminal-success">[OK]</span> Memory headroom: 62% available<br><span class="terminal-success">[OK]</span> P99 latency: 9.4ms across all ingress routes<br><span class="terminal-success">[RESOLVED]</span> Zero anomalous drift detected.`;
            } else if (cmd.includes('helm')) {
                res = `<span class="terminal-prompt">$ ${cmd}</span><br>Release "microservices" has been upgraded. Happy Helming!<br>STATUS: <span class="terminal-success">deployed</span><br>REVISION: 14<br>TEST SUITE: None`;
            }
            out.innerHTML = res;
        }

        // 6. Interactive Syllabus View
        function viewSyllabus(title, details) {
            document.getElementById('modal-title').textContent = title;
            document.getElementById('modal-desc').innerHTML = `<strong>Comprehensive Curriculum:</strong><br>${details}<br><br><span style="color: var(--accent-cyan);">Includes cloud lab instances, certification voucher, and 1-on-1 architecture review.</span>`;
            document.getElementById('checkout-modal').classList.add('open');
        }

        // 7. Estimator Logic
        let estimatorCost = 7500;
        let estimatorWeeks = 5;
        function toggleEstimatorOption(el, cost, weeks) {
            el.classList.toggle('selected');
            calculateEstimator();
        }

        function calculateEstimator() {
            let total = 0;
            let totalW = 2;
            const options = document.querySelectorAll('.estimator-option');
            options.forEach(opt => {
                if (opt.classList.contains('selected')) {
                    if (opt.innerText.includes('Cloud Microservices')) { total += 3000; totalW += 2; }
                    if (opt.innerText.includes('Custom AI Agents')) { total += 4500; totalW += 3; }
                    if (opt.innerText.includes('DevSecOps')) { total += 2500; totalW += 2; }
                    if (opt.innerText.includes('High-Speed API Gateway')) { total += 3500; totalW += 2; }
                }
            });
            document.getElementById('estimator-total').textContent = `$${total.toLocaleString()} • ~${totalW} Weeks Delivery`;
        }

        function requestQuote(service) {
            document.getElementById('modal-title').textContent = `Engineering Quote: ${service}`;
            document.getElementById('modal-desc').innerHTML = `We have initialized a customized architecture scoping session for <strong>${service}</strong>. Our Principal Cloud Engineer will reach out within 2 hours.`;
            document.getElementById('checkout-modal').classList.add('open');
        }

        function openEstimateModal() {
            document.getElementById('modal-title').textContent = "Architecture Scoping Session Booked!";
            document.getElementById('modal-desc').textContent = "Your tailored software development estimate has been submitted to our DevOps engineering architects. Check your inbox for calendar invites.";
            document.getElementById('checkout-modal').classList.add('open');
        }

        // 8. Dynamic Nodes Generation for Telemetry
        const nodeContainer = document.getElementById('nodes-container');
        if (nodeContainer) {
            let nodesHtml = '';
            for (let i = 1; i <= 24; i++) {
                const idStr = i < 10 ? '0' + i : i;
                nodesHtml += `
                    <div class="node-chip">
                        <span>node-k8s-${idStr}</span>
                        <span style="color: #38bdf8; font-size: 0.68rem;">0.8% load</span>
                    </div>
                `;
            }
            nodeContainer.innerHTML = nodesHtml;
        }

        // 9. Live Simulated Telemetry Jitter
        setInterval(() => {
            const cpu = (12 + Math.random() * 4).toFixed(1);
            const ram = (37 + Math.random() * 3).toFixed(1);
            const lat = Math.floor(Math.random() * 4) + 9;
            
            const cpuEl = document.getElementById('stat-cpu');
            const ramEl = document.getElementById('stat-ram');
            const barCpu = document.getElementById('bar-cpu');
            const barRam = document.getElementById('bar-ram');
            const latEl = document.getElementById('telemetry-latency');

            if (cpuEl) cpuEl.textContent = `${cpu}%`;
            if (ramEl) ramEl.textContent = `${ram}%`;
            if (barCpu) barCpu.style.width = `${cpu}%`;
            if (barRam) barRam.style.width = `${ram}%`;
            if (latEl) latEl.textContent = `${lat}ms`;
        }, 3000);

        updateCartUI();
    </script>
</body>
</html>
"""

@app.route('/')
@app.route('/store')
@app.route('/academy')
@app.route('/services')
@app.route('/telemetry')
@app.route('/about')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/health')
def health():
    return jsonify({
        "status": "100% Healthy",
        "service": "AIOps Store & DevStudio",
        "uptime": "99.999%",
        "nodes": "24/24 Online"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

import { useEffect, useMemo, useState } from 'react'
import { Code2, GitBranch, Mail, Network } from 'lucide-react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL || ''
const currentYear = new Date().getFullYear()

const socialLinks = [
  { label: 'GitHub', href: 'https://github.com/hemaharikrishnan178-ops', Icon: GitBranch, external: true },
  { label: 'LinkedIn', href: 'https://www.linkedin.com/in/hema-harikrishnan', Icon: Network, external: true },
  { label: 'LeetCode', href: 'https://leetcode.com/u/hemaharikrishnan/', Icon: Code2, external: true },
  { label: 'Email', href: 'mailto:hemaharikrishnan178@gmail.com', Icon: Mail, external: false },
]

const defaultForm = {
  name: '',
  email: '',
  subject: '',
  message: '',
}

const navItems = [
  { label: 'About', href: '#about' },
  { label: 'Education', href: '#education' },
  { label: 'Skills', href: '#skills' },
  { label: 'Projects', href: '#projects' },
  { label: 'Experience', href: '#experience' },
  { label: 'Contact', href: '#contact' },
]

const experience = [
  {
    title: 'Full-stack problem solving',
    description: 'Building responsive interfaces and backend APIs with a focus on clarity, usability, and maintainable architecture.',
  },
  {
    title: 'AI and product thinking',
    description: 'Exploring how intelligent systems can support real-world needs in areas like agriculture, collaboration, and automation.',
  },
  {
    title: 'Hands-on learning',
    description: 'Working through project-based development, debugging, API design, and deployment workflows to strengthen both technical and communication skills.',
  },
]

const certifications = [
  'Project-led learning in full-stack development',
  'Hackathon-focused problem solving and design thinking',
  'Continuous practice in Python, web development, and AI-driven product ideas',
]

function SocialLinks({ className = 'social-links' }) {
  return (
    <div className={className} aria-label="Social links">
      {socialLinks.map(({ label, href, Icon, external }) => (
        <a
          key={label}
          className="social-link"
          href={href}
          aria-label={label}
          target={external ? '_blank' : undefined}
          rel={external ? 'noreferrer' : undefined}
        >
          <Icon size={18} aria-hidden="true" />
          <span>{label}</span>
        </a>
      ))}
    </div>
  )
}

function App() {
  const [projects, setProjects] = useState([])
  const [skills, setSkills] = useState([])
  const [selectedProject, setSelectedProject] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [form, setForm] = useState(defaultForm)
  const [feedback, setFeedback] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    const loadPortfolioData = async () => {
      try {
        setLoading(true)
        const [projectsResponse, skillsResponse] = await Promise.all([
          fetch(`${API_BASE}/api/projects`),
          fetch(`${API_BASE}/api/skills`),
        ])

        if (!projectsResponse.ok || !skillsResponse.ok) {
          throw new Error('Unable to load portfolio data from the backend.')
        }

        const projectsData = await projectsResponse.json()
        const skillsData = await skillsResponse.json()

        setProjects(projectsData.projects || [])
        setSkills(skillsData.skills || [])
      } catch (loadError) {
        setError(loadError.message)
      } finally {
        setLoading(false)
      }
    }

    loadPortfolioData()
  }, [])

  const groupedSkills = useMemo(() => {
    const groups = {}

    skills.forEach((skill) => {
      const category = skill.category || 'General'
      if (!groups[category]) {
        groups[category] = []
      }
      groups[category].push(skill)
    })

    return Object.entries(groups)
  }, [skills])

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((previous) => ({ ...previous, [name]: value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setSubmitting(true)
    setFeedback(null)

    try {
      const response = await fetch(`${API_BASE}/api/contact`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(form),
      })

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Unable to send message right now.')
      }

      setForm(defaultForm)
      setFeedback({ type: 'success', message: 'Thanks for reaching out. Your message has been sent successfully.' })
    } catch (submitError) {
      setFeedback({ type: 'error', message: submitError.message })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <>
      <header className="site-header">
        <div className="container nav-bar">
          <div className="brand-block">
            <span className="brand-mark">H</span>
            <span className="brand-name">Hema H</span>
          </div>
          <nav className="site-nav" aria-label="Main navigation">
            {navItems.map((item) => (
              <a key={item.href} href={item.href}>
                {item.label}
              </a>
            ))}
          </nav>
          <a className="primary-button button-small" href="/Hema_H_Resume.pdf" download>
            Download Resume
          </a>
        </div>
      </header>

      <main>
        <section className="hero-section">
          <div className="container hero-grid">
            <div className="hero-copy">
              <p className="eyebrow">Portfolio • Full-Stack Learner</p>
              <h1>Crafting thoughtful digital experiences from idea to deployment.</h1>
              <p className="lead">
                I am Hema H, a developer focused on building practical web products, exploring AI-driven
                solutions, and learning by shipping meaningful projects that solve real needs.
              </p>
              <div className="hero-actions">
                <a className="primary-button" href="#projects">
                  View Projects
                </a>
                <a className="secondary-button" href="/Hema_H_Resume.pdf" download>
                  View Resume
                </a>
              </div>
              <ul className="mini-stats" aria-label="Portfolio highlights">
                <li>
                  <strong>2</strong>
                  <span>flagship projects</span>
                </li>
                <li>
                  <strong>Full-stack</strong>
                  <span>learning journey</span>
                </li>
                <li>
                  <strong>AI + web</strong>
                  <span>product focus</span>
                </li>
              </ul>
            </div>

            <div className="hero-panel">
              <div className="panel-card">
                <p className="card-label">Current focus</p>
                <h2>Problem-driven product building</h2>
                <ul>
                  {['Python & JavaScript', 'React & API design', 'Responsive UI systems', 'Database fundamentals'].map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section id="about" className="content-section">
          <div className="container section-heading">
            <p className="section-kicker">About</p>
            <h2>A developer who prefers building with purpose.</h2>
          </div>
          <div className="container about-grid">
            <div className="about-card">
              <p>
                My work is centered on experimentation, iteration, and creating solutions that are both useful
                and understandable. I enjoy exploring how technology can make everyday tasks easier, smarter,
                and more accessible.
              </p>
            </div>
            <div className="about-card">
              <p>
                I am building a strong foundation in frontend engineering, backend development, and product
                thinking with deliberate focus on clean code, clear communication, and practical implementation.
              </p>
            </div>
          </div>
        </section>

        <section id="education" className="content-section alt-section">
          <div className="container section-heading">
            <p className="section-kicker">Education</p>
            <h2>Academic background.</h2>
          </div>
          <div className="container about-grid">
            <div className="about-card">
              <p>For education history and qualifications, please refer to my downloadable resume.</p>
              <a className="text-button" href="/Hema_H_Resume.pdf" target="_blank" rel="noreferrer">
                Open resume
              </a>
            </div>
          </div>
        </section>

        <section id="skills" className="content-section alt-section">
          <div className="container section-heading">
            <p className="section-kicker">Skills</p>
            <h2>Tools, technologies, and learning areas.</h2>
          </div>
          <div className="container skills-grid">
            {loading ? (
              <p className="status-text">Loading skills...</p>
            ) : groupedSkills.length > 0 ? (
              groupedSkills.map(([category, skillList]) => (
                <div key={category} className="skill-group">
                  <h3>{category}</h3>
                  <div className="chip-list">
                    {skillList.map((skill) => (
                      <span key={`${category}-${skill.name}`} className="skill-chip">
                        {skill.name}
                      </span>
                    ))}
                  </div>
                </div>
              ))
            ) : (
              <p className="status-text">Skill data is not available yet.</p>
            )}
          </div>
        </section>

        <section id="projects" className="content-section">
          <div className="container section-heading inline-heading">
            <div>
              <p className="section-kicker">Projects</p>
              <h2>Key work and product concepts.</h2>
            </div>
          </div>

          <div className="container project-grid">
            {loading ? (
              <p className="status-text">Loading projects...</p>
            ) : projects.length > 0 ? (
              projects.map((project) => (
                <article className="project-card" key={project.id || project.slug}>
                  <div className="project-topline">
                    <span className="project-badge">{project.category}</span>
                  </div>
                  <h3>{project.title}</h3>
                  <p>{project.description}</p>
                  <div className="project-techs">
                    {(project.technologies || []).slice(0, 4).map((tech) => (
                      <span key={tech}>{tech}</span>
                    ))}
                  </div>
                  <button type="button" className="text-button" onClick={() => setSelectedProject(project)}>
                    View details
                  </button>
                </article>
              ))
            ) : (
              <p className="status-text">Project data is not available yet.</p>
            )}
          </div>
        </section>

        <section id="experience" className="content-section alt-section">
          <div className="container section-heading">
            <p className="section-kicker">Experience</p>
            <h2>Focused on hands-on, product-minded learning.</h2>
          </div>
          <div className="container experience-grid">
            {experience.map((item) => (
              <article key={item.title} className="experience-card">
                <div className="experience-index">0{experience.indexOf(item) + 1}</div>
                <h3>{item.title}</h3>
                <p>{item.description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="content-section">
          <div className="container section-heading">
            <p className="section-kicker">Learning & recognition</p>
            <h2>Continuous growth through practice and collaboration.</h2>
          </div>
          <div className="container certifications-grid">
            {certifications.map((item) => (
              <div key={item} className="cert-card">
                <span className="cert-icon">✦</span>
                <p>{item}</p>
              </div>
            ))}
          </div>
        </section>

        <section id="contact" className="content-section contact-section">
          <div className="container contact-grid">
            <div>
              <p className="section-kicker">Contact</p>
              <h2>Let’s build something useful together.</h2>
              <p className="contact-copy">
                Whether you are looking for collaboration, a project discussion, or a chance to work on an idea
                with purpose, I would be glad to hear from you.
              </p>
              <SocialLinks />
            </div>

            <form className="contact-form" onSubmit={handleSubmit}>
              <div className="field-row">
                <label>
                  <span>Name</span>
                  <input type="text" name="name" value={form.name} onChange={handleChange} required />
                </label>
                <label>
                  <span>Email</span>
                  <input type="email" name="email" value={form.email} onChange={handleChange} required />
                </label>
              </div>

              <label>
                <span>Subject</span>
                <input type="text" name="subject" value={form.subject} onChange={handleChange} required />
              </label>

              <label>
                <span>Message</span>
                <textarea name="message" value={form.message} onChange={handleChange} required rows="5" />
              </label>

              <button type="submit" className="primary-button" disabled={submitting}>
                {submitting ? 'Sending...' : 'Send Message'}
              </button>

              {feedback && <p className={`form-feedback ${feedback.type}`}>{feedback.message}</p>}
              {error && <p className="form-feedback error">{error}</p>}
            </form>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <div className="container footer-content">
          <p>© {currentYear} Hema H</p>
          <SocialLinks className="social-links footer-social-links" />
        </div>
      </footer>

      {selectedProject && (
        <div className="modal-backdrop" onClick={() => setSelectedProject(null)}>
          <div className="project-modal" onClick={(event) => event.stopPropagation()}>
            <button type="button" className="close-button" onClick={() => setSelectedProject(null)} aria-label="Close project details">
              ×
            </button>
            <p className="modal-tag">{selectedProject.category}</p>
            <h3>{selectedProject.title}</h3>
            <p>{selectedProject.description}</p>
            <div className="project-techs modal-techs">
              {(selectedProject.technologies || []).map((tech) => (
                <span key={`${selectedProject.slug}-${tech}`}>{tech}</span>
              ))}
            </div>
            <div className="modal-links">
              {selectedProject.repository_url && (
                <a href={selectedProject.repository_url} target="_blank" rel="noreferrer">
                  Repository
                </a>
              )}
              {selectedProject.demo_url && (
                <a href={selectedProject.demo_url} target="_blank" rel="noreferrer">
                  Live Demo
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default App

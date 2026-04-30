import axios from 'axios'

const client = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const isAdminRoute = window.location.pathname.startsWith('/admin')
      if (isAdminRoute && window.location.pathname !== '/admin') {
        localStorage.removeItem('admin_token')
        window.location.href = '/admin'
      }
    }
    return Promise.reject(error)
  }
)

export const api = {
  // Profile
  getProfile: () => client.get('/profile/'),
  updateProfile: (data) => client.put('/profile/', data),

  // Experience
  getExperience: () => client.get('/experience/'),
  createExperience: (data) => client.post('/experience/', data),
  updateExperience: (id, data) => client.put(`/experience/${id}`, data),
  deleteExperience: (id) => client.delete(`/experience/${id}`),

  // Education
  getEducation: () => client.get('/education/'),
  createEducation: (data) => client.post('/education/', data),
  updateEducation: (id, data) => client.put(`/education/${id}`, data),
  deleteEducation: (id) => client.delete(`/education/${id}`),

  // Skills
  getSkills: () => client.get('/skills/'),
  createSkill: (data) => client.post('/skills/', data),
  updateSkill: (id, data) => client.put(`/skills/${id}`, data),
  deleteSkill: (id) => client.delete(`/skills/${id}`),

  // Certifications
  getCertifications: () => client.get('/certifications/'),
  createCertification: (data) => client.post('/certifications/', data),
  updateCertification: (id, data) => client.put(`/certifications/${id}`, data),
  deleteCertification: (id) => client.delete(`/certifications/${id}`),

  // Projects
  getProjects: () => client.get('/projects/'),
  createProject: (data) => client.post('/projects/', data),
  updateProject: (id, data) => client.put(`/projects/${id}`, data),
  deleteProject: (id) => client.delete(`/projects/${id}`),

  // Research
  getResearch: () => client.get('/research/'),
  createResearch: (data) => client.post('/research/', data),
  updateResearch: (id, data) => client.put(`/research/${id}`, data),
  deleteResearch: (id) => client.delete(`/research/${id}`),

  // Awards
  getAwards: () => client.get('/awards/'),
  createAward: (data) => client.post('/awards/', data),
  updateAward: (id, data) => client.put(`/awards/${id}`, data),
  deleteAward: (id) => client.delete(`/awards/${id}`),

  // Impact
  getImpact: () => client.get('/impact/'),
  createImpact: (data) => client.post('/impact/', data),
  updateImpact: (id, data) => client.put(`/impact/${id}`, data),
  deleteImpact: (id) => client.delete(`/impact/${id}`),

  // Auth
  login: (username, password) => client.post('/auth/login', { username, password }),
  getMe: () => client.get('/auth/me'),
}

export default client

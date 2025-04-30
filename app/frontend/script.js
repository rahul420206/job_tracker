const api = 'http://127.0.0.1:8000';

async function register() {
  const username = document.getElementById('register-username').value;
  const password = document.getElementById('register-password').value;
  const role = document.getElementById('register-role').value;

  const res = await fetch(`${api}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, role })
  });

  alert(res.ok ? 'Registered successfully!' : 'Registration failed');
}

async function login() {
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);

  const res = await fetch(`${api}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params
  });

  if (res.ok) {
    const data = await res.json();
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('username', username);
    window.location.href = 'dashboard.html';
  } else {
    alert('Login failed');
  }
}

// DASHBOARD LOGIC
if (window.location.pathname.includes('dashboard.html')) {
  const token = localStorage.getItem('token');
  const username = localStorage.getItem('username');

  document.getElementById('welcome-msg').innerText = `Welcome, ${username}!`;

  fetch(`${api}/users/me`, {
    headers: { Authorization: `Bearer ${token}` }
  }).then(res => res.json()).then(user => {
    if (user.role === 'recruiter') {
      document.getElementById('post-job-form').style.display = 'block';
    }
  });

  fetch(`${api}/jobs/`, {
    headers: { Authorization: `Bearer ${token}` }
  })
    .then(res => res.json())
    .then(jobs => {
      const list = document.getElementById('job-list');
      jobs.forEach(job => {
        const div = document.createElement('div');
        div.innerHTML = `
          <h4>${job.title} at ${job.company}</h4>
          <p>${job.description}</p>
          <p><strong>Location:</strong> ${job.location}</p>
          <button onclick="applyToJob(${job.id})">Apply</button>
          <hr>
        `;
        list.appendChild(div);
      });
    });
}

async function postJob() {
  const title = document.getElementById('job-title').value;
  const description = document.getElementById('job-desc').value;
  const location = document.getElementById('job-location').value;
  const company = document.getElementById('job-company').value;
  const token = localStorage.getItem('token');

  await fetch(`${api}/jobs/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ title, description, location, company })
  });

  alert('Job posted!');
  location.reload();
}

async function applyToJob(jobId) {
  const token = localStorage.getItem('token');
  const res = await fetch(`${api}/jobs/${jobId}/apply`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  alert(res.ok ? 'Applied successfully!' : 'Could not apply');
}

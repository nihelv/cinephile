// 로그인, 회원가입 axios
const loginForm = document.getElementById('login-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
const username = document.getElementsByName('username')
const password = document.getElementsByName('password')
const errorModal = document.getElementById('error-modal')
const errorText = document.getElementsByClassName('error-text')

loginForm.addEventListener('submit', function (event) {
  event.preventDefault()
  const formData = new FormData()
  formData.append('username', username[0].value)
  formData.append('password', password[0].value)
  formData.append('csrfmiddlewaretoken', csrftoken)

  axios({
    method: 'post',
    url: '/accounts/login/',
    headers: {'X-CSRFToken': csrftoken},
    data: formData,
  })
  .then((response) => {
    if (response.data.valid) {
      location.reload()
    } else {
      errorModal.style.display = 'flex'
      errorText[0].textContent = response.data.error['__all__']
      // alert(response.data.error['__all__'])
      password[0].value = ''
    }
  })
})

const signupForm = document.getElementById('signup-form')
const email = document.getElementsByName('email')
const firstName = document.getElementsByName('first_name')
const lastName = document.getElementsByName('last_name')
const password1 = document.getElementsByName('password1')
const password2 = document.getElementsByName('password2')

signupForm.addEventListener('submit', function (event) {
  event.preventDefault()
  const formData = new FormData()
  formData.append('username', username[1].value)
  formData.append('email', email[0].value)
  formData.append('first_name', firstName[0].value)
  formData.append('last_name', lastName[0].value)
  formData.append('password1', password1[0].value)
  formData.append('password2', password2[0].value)
  formData.append('csrfmiddlewaretoken', csrftoken)

  axios({
    method: 'post',
    url: '/accounts/signup/',
    headers: {'X-CSRFToken': csrftoken},
    data: formData,
  })
  .then((response) => {
    if (response.data.valid) {
      location.reload()
    } else {
      errorModal.style.display = 'flex'
      errorText[0].textContent = response.data.error[response.data.error_field]
      // alert(response.data.error[response.data.error_field])
      password1[0].value = ''
      password2[0].value = ''
    }
  })
})

// 오류 모달
const closeBtn = document.querySelector('.close-area')

closeBtn.addEventListener('click', function(event) {
  errorModal.style.display = 'none'
})

errorModal.addEventListener('click', function (event) {
  const eventTarget = event.target
  if (eventTarget.classList.contains('modal-overlay')) {
    errorModal.style.display = 'none'
  }
})
// 스크롤 방향에 따라 움직이는 헤더
const header = document.querySelector('.header')
const profileWrapper = document.querySelector('.profile-wrap')
let prevScrollTop = 0

const headerMoving = function(direction) {
  if (direction == 'up') {
    header.classList.remove('nav-up')
    if (profileWrapper) {
      profileWrapper.classList.remove('profile-up')
    }
  } else {
    header.classList.add('nav-up')
    if (profileWrapper) {
      profileWrapper.classList.add('profile-up')
    }
  }
}

document.addEventListener('scroll', function() {
  let nextScrollTop = window.pageYOffset
  if (nextScrollTop > prevScrollTop) {
    headerMoving('down')
  } else if (nextScrollTop < prevScrollTop) {
    headerMoving('up')
  }

  prevScrollTop = nextScrollTop
})

// 검색어
function Slider(target) {
  let index = 1;
  let isMoved = true;
  const speed = 1500; // ms

  const transform = "transform " + speed / 1000 + "s";
  let translate = (i) => "translateY(-" + 100 * i + "%)";

  const slider = document.querySelector(target);
  const sliderRects = slider.getClientRects()[0];
  slider.style["overflow"] = "hidden";

  const container = document.createElement("div");
  container.style["display"] = "flex";
  container.style["flex-direction"] = "column";
  container.style["width"] = sliderRects.width + "px";
  container.style["height"] = 24 + "px";
  container.style["transform"] = translate(index);

  let boxes = [].slice.call(slider.children);
  boxes = [].concat(boxes[boxes.length - 1], boxes, boxes[0]);

  const size = boxes.length;
  for (let i = 0; i < size; i++) {
    const box = boxes[i];
    if (i === 11) {
      box.children[0].textContent = 1
    } else {
      box.children[0].textContent = i
    }
    box.style["height"] = "100%";
    box.style["width"] = "100%";
    container.appendChild(box.cloneNode(true));
  }

  container.addEventListener("transitionstart", function () {
    isMoved = false;
    setTimeout(() => {
      isMoved = true;
    }, speed);
  });
  container.addEventListener("transitionend", function () {
    if (index === size - 1) {
      index = 1;
      container.style["transition"] = "none";
      container.style["transform"] = translate(index);
    }
    if (index === 0) {
      index = size - 1;
      container.style["transition"] = "none";
      container.style["transform"] = translate(index);
    }
  });

  slider.innerHTML = "";
  slider.appendChild(container);

  return {
    move: function (i) {
      if (isMoved === true) {
        index = i;
        container.style["transition"] = transform;
        container.style["transform"] = translate(index);
      }
    },
    next: function () {
      if (isMoved === true) {
        index = (index + 1) % size;
        container.style["transition"] = transform;
        container.style["transform"] = translate(index);
      }
    },
    prev: function () {
      if (isMoved === true) {
        index = index === 0 ? index + size : index;
        index = (index - 1) % size;
        container.style["transition"] = transform;
        container.style["transform"] = translate(index);
      }
    }
  };
}

const s1 = new Slider("#slider");

setInterval(() => {
  s1.next();
}, 1500)

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
const password1 = document.getElementsByName('password1')
const password2 = document.getElementsByName('password2')

signupForm.addEventListener('submit', function (event) {
  event.preventDefault()
  const formData = new FormData()
  formData.append('username', username[1].value)
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
        alert(response.data.error[response.data.error_field])
        password1[0].value = ''
        password2[0].value = ''
      }
    })
})

// 팔로우 axios
const followForms = document.querySelectorAll('.follow-form')
const followingCountTag = document.getElementById('following-count')
const followerCountTag = document.getElementById('follower-count')


followForms.forEach((followForm) => {
  followForm.addEventListener('submit', function (event) {
    event.preventDefault()
    const userId = event.target.dataset.userId
    axios({
      method: 'post',
      url: `/accounts/${userId}/follow/`,
      headers: {'X-CSRFToken': csrftoken},
    })
      .then((response) => {
        const isFollowed = response.data.is_followed
        const followBtn = document.querySelector('.follow-form > input[type=submit]')
        console.log(isFollowed)
        if (isFollowed) {
          followBtn.value = '언팔로우'
          followBtn.classList.add('main-outline-btn')
          followBtn.classList.remove('main-btn')
        } else {
          followBtn.value = '팔로우'
          followBtn.classList.add('main-btn')
          followBtn.classList.remove('main-outline-btn')
        }

        const followingCountData = response.data.following_count
        const followerCountData = response.data.follower_count

        followingCountTag.textContent = followingCountData
        followerCountTag.textContent = followerCountData
      })
  })
})
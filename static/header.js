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
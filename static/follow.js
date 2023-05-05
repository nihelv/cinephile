// 팔로우 axios
const followForm = document.querySelector('.follow-form')
const followingCountTag = document.getElementById('following-count')
const followerCountTag = document.getElementById('follower-count')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

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
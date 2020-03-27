document.addEventListener('DOMContentLoaded', function () {
  let trigger = document.querySelector('.dropdown-trigger')
  trigger.onclick = dropdown
  let recording = document.querySelector('.o-play-btn')
  recording.onclick = record
});

function dropdown() {
  let categories = document.querySelector(".box")
  categories.classList.toggle("is-open")
  categories.onclick = function (event) {
    let category = getCategory(event).innerHTML
    let articleApi = "http://127.0.0.1:5000/api/article"
    let method = "POST"
    let requestBody = {
      "category": category
    }
    getArticleData(articleApi, requestBody, method)
    categories.classList.remove("is-open")
    let trigger = document.querySelector('.dropdown-trigger')
    trigger.innerHTML = category
  }
}

function getCategory(e) {
  e = e || window.event;
  return e.target || e.srcElement;
}

function getArticleData(api, requestBody, method) {
  let request = new XMLHttpRequest()
  console.log(requestBody)
  request.open(method, api, true)
  request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  request.send(JSON.stringify(requestBody))

  request.onload = function () {
    let index = 0
    let articleData = JSON.parse(this.response)
    if (request.status >= 200 && request.status < 400) {
      console.log(articleData)
      setArticleView(articleData["title"], articleData["url"], articleData["sentences"][index])
      let progressBar = document.querySelector("#progress-bar")
      let buttonNext = document.querySelector("#button-next")
      let buttonBack = document.querySelector("#button-back")

      progressBar.setAttribute("max", articleData["total_sentences"])
      
      buttonNext.onclick = function (event) {
        index++
        if (index >= articleData["total_sentences"]) {
          index = articleData["total_sentences"] - 1;
        }
        progressBar.setAttribute("value", index+1)
        setArticleView(articleData["title"], articleData["url"], articleData["sentences"][index])
      }
      
      buttonBack.onclick = function (event) {
        index--
        if (index < 0) {
          index = 0
        }
        progressBar.setAttribute("value", index-1) 
        setArticleView(articleData["title"], articleData["url"], articleData["sentences"][index])
      }
    } else {
      console.log('error')
    }
  }
  // request.send()
}

function setArticleView(title, url, sentence) {
  let articleTitle = document.querySelector("#article-title")
  let articleUrl = document.querySelector("#article-url")
  let articleSentence = document.querySelector("#article-sentence")
  articleTitle.innerHTML = title
  articleUrl.innerHTML = url
  articleUrl.setAttribute("href", url) 
  articleSentence.innerHTML = sentence
}

function record() {
  let recording = document.querySelector('.o-play-btn')
  recording.classList.toggle('o-play-btn--playing')
}

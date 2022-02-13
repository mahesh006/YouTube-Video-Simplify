
const insightsButton = document.querySelector('#videocaption');
const popup = document.querySelector('.popup-content');

const loader = document.querySelector('.loader');

const youtubesubtitle = document.getElementById('youtube_icon_subtitle');

const subtitles = document.getElementById('vid_subtitles');
const topics = document.getElementById('topics');



let currentTabURL;








chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    currentTabURL = tabs[0].url;
  
});



async function youtube_video_subtitle(url = '', data) {
    document.getElementById('youtube_subtitle').style.display = 'none';
    document.getElementById('hides').style.display = 'none';
    loading(true);
    //console.log('value');
    //console.log(currentTabURL);

    try {
        // Default options are marked with *
       const response = await fetch(url, {
           method: 'POST', // *GET, POST, PUT, DELETE, etc.
           mode: 'cors', // no-cors, *cors, same-origin
           cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
           credentials: 'same-origin', // include, *same-origin, omit
           headers: {
           'Content-Type': 'application/json'
           // 'Content-Type': 'application/x-www-form-urlencoded',
           },
           redirect: 'follow', // manual, *follow, error
           referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
           body: JSON.stringify(data) // body data type must match "Content-Type" header
       });
       return response.json(); 
       //const responseData = await response.json();// parses JSON response into native JavaScript objects
       //const { data } = responseData;
       
       //console.log(data)
       
   }
   catch(err) {
       console.log(err)
       //document.getElementsByClassName('error404').style.display = 'block';
   } 
    
};





youtubesubtitle.addEventListener('click', () => {
    var video_id = currentTabURL
    console.log(video_id)
    youtube_video_subtitle('http://127.0.0.1:5000/video', video_id)
    .then(data => {
        loading(false);       
        changeDisplay(popup, 'none');
        document.getElementById('youtube_subtitle').style.display = 'block';
        document.getElementById('hides').style.display = 'block';
        console.log(data);
        //conversationId = data.data;
       
        
        if (data) {       // JSON data parsed by `data.json()` call
          //  console.log(data);
            subtitles.innerHTML = 'Summary:  ' + data[0].data;
            topics.innerHTML = 'Summary Topics:  ' + data[1].topics;

        } 
    });

});




// @Func: Change display property of element
export const changeDisplay = (element, type) => {
    if (type) {
        element.style.display = type;
        return;
    }
    element.style.display =
        element.style.display === 'none'
            ? 'block'
            : element.style.display === 'block'
            ? 'none'
            : 'none';
    return;
};


const videosearch = () => {
    changeDisplay(popup, 'none');

    //document.getElementById('youtube_seach').style.display = 'block';
    document.getElementById('youtube_subtitle').style.display = 'block';
    //document.getElementById('hide').style.display = 'block';
    document.getElementById('hides').style.display = 'block';

    
    //console.log('working')
}



insightsButton.addEventListener('click', videosearch);



// Loading Function

export const loading = (status) => {
    if (status) {
        changeDisplay(loader, 'block');
        //changeDisplay(checkButton);
        return;
    }

    changeDisplay(loader, 'none');
    //closePreviewFn();
    return;
};




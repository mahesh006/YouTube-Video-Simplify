const URL = window.location.toString();

chrome.runtime.sendMessage(
    {
        message: 'checkURL',
        URL
    },
    (res) => {
        console.log(res);
    }
);

chrome.runtime.onMessage.addListener((req, sender, res) => {
    console.log(req);
});
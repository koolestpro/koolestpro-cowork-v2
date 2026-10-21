// Paste into the Chrome DevTools Console on your TikTok collection page (while logged in).
// It scrolls to the end, then copies every video link to your clipboard.
// Save the clipboard as references-for-posts/video-inspo/tiktok/links.txt
(async()=>{const s=new Set();let last=0,stable=0;
for(let i=0;i<80&&stable<4;i++){window.scrollTo(0,document.body.scrollHeight);
await new Promise(r=>setTimeout(r,1500));
document.querySelectorAll('a[href*="/video/"]').forEach(a=>s.add(a.href.split('?')[0]));
if(s.size===last)stable++;else{stable=0;last=s.size}}
copy([...s].join('\n'));console.log(s.size+' links copied')})();

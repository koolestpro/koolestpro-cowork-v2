"""QA: per-slide text overflow, content-vs-footer collision, empty bands, swipe click-through, console errors."""
import asyncio, sys, os, json
sys.path.insert(0, os.path.abspath('.ai-workflow/tools'))
from playwright.async_api import async_playwright
from sandbox_cdn_route import install_routes_async
async def main(files):
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--no-sandbox"])
        for f in files:
            pg=await b.new_page(viewport={"width":1200,"height":1000}); errs=[]
            pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await install_routes_async(pg)
            await pg.goto("file://"+os.path.abspath(f), wait_until="domcontentloaded"); await pg.wait_for_timeout(3000)
            await pg.evaluate("document.getElementById('stage').style.transform='none'")
            r=await pg.evaluate("""()=>[...document.querySelectorAll('.slide')].map((s,i)=>{
              const sr=s.getBoundingClientRect(); const out=[];
              s.querySelectorAll('.h,.body,.cap,.pill').forEach(e=>{const r=e.getBoundingClientRect();
                if(e.scrollWidth>e.clientWidth+2) out.push('hscroll:'+e.textContent.slice(0,30));
                if(r.right>sr.left+1080-40+1||r.left<sr.left+40) out.push('xedge:'+e.textContent.slice(0,30));
                if(r.bottom>sr.top+1350-110) out.push('intofooter:'+e.textContent.slice(0,30)+':'+Math.round(r.bottom-sr.top));
                if(e.classList.contains('h')){const lh=parseFloat(getComputedStyle(e).lineHeight)||parseFloat(getComputedStyle(e).fontSize);
                  const brs=(e.innerHTML.match(/<br>/g)||[]).length+1; const lines=Math.round(r.height/lh); if(lines>brs) out.push(`wrap:${lines}>${brs}:`+e.textContent.slice(0,30));}
              });
              const inn=s.querySelector('.in'); const last=[...inn.children].pop(); const lb=last.getBoundingClientRect().bottom-sr.top;
              return {slide:i+1, issues:out, lastBottom:Math.round(lb)};})""")
            await pg.evaluate("document.getElementById('stage').style.transform=''")
            # click-through via swipe control
            n=await pg.evaluate("TOTAL"); seen=[]
            for i in range(n):
                seen.append(await pg.inner_text('#pager'))
                if i<n-1: await pg.click('#main-swb')
                await pg.wait_for_timeout(250)
            divs=await pg.evaluate("""()=>{const h=document.documentElement.outerHTML;return [(h.match(/<div/g)||[]).length,(h.match(/<\\/div>/g)||[]).length]}""")
            print(os.path.basename(f), json.dumps(r), "pager:",seen, "errors:",errs)
            await pg.close()
        await b.close()
asyncio.run(main(sys.argv[1:]))

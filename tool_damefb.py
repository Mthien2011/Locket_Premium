// ==UserScript==
// @name         Auto Dame FB t.me/thegioiios
// @namespace    http://tampermonkey.net/
// @version      13.2
// @description  Auto Dame FB @thegioiios - Tốc độ 0.9s - Fix lỗi hiển thị
// @author       Miuka_cracker
// @match        https://www.facebook.com/*
// @grant        none
// ==/UserScript==

(async () => {
    'use strict';

    // Kênh Telegram : https://t.me/thegioiios
    // ==========================================
    // THÊM HÀM KIỂM TRA VÀ FIX LỖI HIỂN THỊ
    // ==========================================
    async function checkAndFixDisplay() {
        // Kiểm tra nếu trang bị lỗi hiển thị (chữ Trung Quốc)
        if (document.body.innerText.includes('下载') || document.title.includes('下载')) {
            console.log('⚠️ Phát hiện lỗi hiển thị, đang refresh...');
            
            // Tạo thông báo
            const notice = document.createElement('div');
            notice.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: red;
                color: white;
                padding: 20px;
                border-radius: 10px;
                z-index: 9999999;
                font-size: 20px;
                font-weight: bold;
            `;
            notice.innerText = '⚠️ Phát hiện lỗi hiển thị - Đang tự động refresh...';
            document.body.appendChild(notice);
            
            // Đợi 2 giây rồi refresh
            await new Promise(r => setTimeout(r, 2000));
            window.location.reload();
            return true;
        }
        return false;
    }

    // ==========================================
    // GIỮ NGUYÊN TOÀN BỘ CODE CŨ CỦA BẢN 13.1
    // ==========================================
    
    // CẤU HÌNH CƠ BẢN & XPATH CHUẨN
    const INPUT_XPATH = "//*[@aria-label=\"Facebook Page name or URL\"]";

    // XPath bắn tỉa vào class 'xdj266r'
    const XP_SUBMIT = "//div[contains(@class, 'xdj266r')]//span[contains(text(), 'Submit') or contains(text(), 'Gửi')]";
    const XP_DONE   = "//div[contains(@class, 'xdj266r')]//span[contains(text(), 'Done') or contains(text(), 'Xong') or contains(text(), 'Hoàn tất')]";
    const XP_NEXT   = "//div[contains(@class, 'xdj266r')]//span[contains(text(), 'Next') or contains(text(), 'Tiếp')]";

    // DANH SÁCH 65 BƯỚC
    const steps = [
        // --- CỤM 1: Fake Profile ---
        { "step": 1, "name": "Menu (3 chấm)", "xpath": "//*[@aria-label=\"Profile settings see more options\"]" },
        { "step": 2, "name": "Report profile", "xpath": "//SPAN[contains(text(), \"Report profile\")]" },
        { "step": 3, "name": "Something about this profile", "xpath": "//SPAN[contains(text(), \"Something about this profile\")]" },
        { "step": 4, "name": "Fake profile", "xpath": "//SPAN[contains(text(), \"Fake profile\")]" },
        { "step": 5, "name": "They’re not a real person", "xpath": "//SPAN[contains(text(), \"They’re not a real person\")]" },
        { "step": 6, "name": "Submit", "xpath": XP_SUBMIT },
        { "step": 7, "name": "Next", "xpath": XP_NEXT },
        { "step": 8, "name": "Done", "xpath": XP_DONE },

        // --- CỤM 2: Celebrity Meta ---
        { "step": 9, "name": "Menu (3 chấm)", "xpath": "//*[@aria-label=\"Profile settings see more options\"]" },
        { "step": 10, "name": "Report profile", "xpath": "//SPAN[contains(text(), \"Report profile\")]" },
        { "step": 11, "name": "Something about this profile", "xpath": "//SPAN[contains(text(), \"Something about this profile\")]" },
        { "step": 12, "name": "Fake profile", "xpath": "//SPAN[contains(text(), \"Fake profile\")]" },
        { "step": 13, "name": "A celebrity or public figure", "xpath": "//SPAN[contains(text(), \"A celebrity or public figure\")]" },
        { "step": 14, "name": "NHẬP TÊN: Meta", "xpath": INPUT_XPATH, "inputData": "Meta" },
        { "step": 15, "name": "Click Chọn Meta", "specialAction": "CLICK_META_RESULT" },
        { "step": 16, "name": "Next", "xpath": XP_NEXT },
        { "step": 17, "name": "Submit", "xpath": XP_SUBMIT },
        { "step": 18, "name": "Next", "xpath": XP_NEXT },
        { "step": 19, "name": "Done", "xpath": XP_DONE },

        // --- CỤM 3: Under 18 ---
        { "step": 20, "name": "Menu (3 chấm)", "xpath": "//*[@aria-label=\"Profile settings see more options\"]" },
        { "step": 21, "name": "Report profile", "xpath": "//SPAN[contains(text(), \"Report profile\")]" },
        { "step": 22, "name": "Something about this profile", "xpath": "//SPAN[contains(text(), \"Something about this profile\")]" },
        { "step": 23, "name": "Problem involving someone under 18", "xpath": "//SPAN[contains(text(), \"Problem involving someone under 18\")]" },
        { "step": 24, "name": "Physical abuse", "xpath": "//SPAN[contains(text(), \"Physical abuse\")]" },
        { "step": 25, "name": "Submit", "xpath": XP_SUBMIT },
        { "step": 26, "name": "Next", "xpath": XP_NEXT },
        { "step": 27, "name": "Done", "xpath": XP_DONE },

        // --- CỤM 4: Violent ---
        { "step": 28, "name": "Menu (3 chấm)", "xpath": "//*[@aria-label=\"Profile settings see more options\"]" },
        { "step": 29, "name": "Report profile", "xpath": "//SPAN[contains(text(), \"Report profile\")]" },
        { "step": 30, "name": "Something about this profile", "xpath": "//SPAN[contains(text(), \"Something about this profile\")]" },
        { "step": 31, "name": "Violent, hateful content", "xpath": "//SPAN[contains(text(), \"Violent, hateful or disturbing content\")]" },
        { "step": 32, "name": "Credible threat to safety", "xpath": "//SPAN[contains(text(), \"Credible threat to safety\")]" },
        { "step": 33, "name": "Submit", "xpath": XP_SUBMIT },
        { "step": 34, "name": "Next", "xpath": XP_NEXT },
        { "step": 35, "name": "Done", "xpath": XP_DONE },

        // --- CỤM 5: Scam (Fraud) ---
        { "step": 36, "name": "Menu (3 chấm)", "xpath": "//*[@aria-label=\"Profile settings see more options\"]" },
        { "step": 37, "name": "Report profile", "xpath": "//SPAN[contains(text(), \"Report profile\")]" },
        { "step": 38, "name": "Something about this profile", "xpath": "//SPAN[contains(text(), \"Something about this profile\")]" },
        { "step": 39, "name": "Scam, fraud", "xpath": "//SPAN[contains(text(), \"Scam, fraud or false information\")]" },
        { "step": 40, "name": "Fraud or scam", "xpath": "//SPAN[contains(text(), \"Fraud or scam\")]" },
        { "step": 41, "name": "Submit", "xpath": XP_SUBMIT },
        { "step": 42, "name": "Next", "xpath": XP_NEXT },
        { "step": 43, "name": "Done", "xpath": XP_DONE },

        // --- CỤM 6: Scam (Spam) ---
        { "step": 44, "name": "Menu (3 chấm)", "xpath": "//*[@aria-label=\"Profile settings see more options\"]" },
        { "step": 45, "name": "Report profile", "xpath": "//SPAN[contains(text(), \"Report profile\")]" },
        { "step": 46, "name": "Something about this profile", "xpath": "//SPAN[contains(text(), \"Something about this profile\")]" },
        { "step": 47, "name": "Scam, fraud", "xpath": "//SPAN[contains(text(), \"Scam, fraud or false information\")]" },
        { "step": 48, "name": "Spam", "xpath": "//SPAN[contains(text(), \"Spam\")]" },
        { "step": 49, "name": "Done", "xpath": XP_DONE },

        // --- CỤM 7: Something else ---
        { "step": 50, "name": "Menu (3 chấm)", "xpath": "//*[@aria-label=\"Profile settings see more options\"]" },
        { "step": 51, "name": "Report profile", "xpath": "//SPAN[contains(text(), \"Report profile\")]" },
        { "step": 52, "name": "Something about this profile", "xpath": "//SPAN[contains(text(), \"Something about this profile\")]" },
        { "step": 53, "name": "Something else", "xpath": "//SPAN[contains(text(), \"Something else\")]" },
        { "step": 54, "name": "Done", "xpath": XP_DONE },

        // --- CỤM 8: Fake Celebrity MARK ZUCKERBERG ---
        { "step": 55, "name": "Menu (3 chấm)", "xpath": "//*[@aria-label=\"Profile settings see more options\"]" },
        { "step": 56, "name": "Report profile", "xpath": "//SPAN[contains(text(), \"Report profile\")]" },
        { "step": 57, "name": "Something about this profile", "xpath": "//SPAN[contains(text(), \"Something about this profile\")]" },
        { "step": 58, "name": "Fake profile", "xpath": "//SPAN[contains(text(), \"Fake profile\")]" },
        { "step": 59, "name": "A celebrity or public figure", "xpath": "//SPAN[contains(text(), \"A celebrity or public figure\")]" },
        { "step": 60, "name": "NHẬP TÊN: Mark Zuckerberg", "xpath": INPUT_XPATH, "inputData": "Mark Zuckerberg" },
        { "step": 61, "name": "Click Mark Zuckerberg", "specialAction": "CLICK_MARK_ZUCKERBERG_RESULT" },
        { "step": 62, "name": "Next", "xpath": XP_NEXT },
        { "step": 63, "name": "Submit", "xpath": XP_SUBMIT },
        { "step": 64, "name": "Next", "xpath": XP_NEXT },
        { "step": 65, "name": "Done", "xpath": XP_DONE }
    ];

    // [TURBO MODE] Điều chỉnh thời gian
    const DELAY_TIME = 900;        // 0.9 giây
    const INPUT_DELAY = 1500;      // 1.5 giây cho input
    const SHORT_DELAY = 300;       // Delay ngắn 0.3 giây

    // ==========================================
    // CORE ENGINE
    // ==========================================
    const sleep = ms => new Promise(r => setTimeout(r, ms));

    function getElementByXpath(path) {
        if (!path) return null;
        return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    }

    function safeClick(element) {
        if (!element) return;
        let blocker = element.closest('[aria-hidden="true"]');
        if (blocker) blocker.removeAttribute('aria-hidden');
        element.scrollIntoView({block: "center", inline: "center"});
        const opts = { bubbles: true, cancelable: true, view: window };
        element.dispatchEvent(new MouseEvent('mousedown', opts));
        element.dispatchEvent(new MouseEvent('mouseup', opts));
        element.dispatchEvent(new MouseEvent('click', opts));
    }

    // Hàm chỉ click trong popup report
    function findButtonInsideDialog(keywords) {
        let dialog = document.querySelector('div[role="dialog"]');
        if (!dialog) return null;

        let all = dialog.querySelectorAll(
            'div[role="button"], button, span'
        );

        all = [...all].filter(el =>
            el.offsetParent !== null &&
            el.offsetWidth > 0
        );

        for (let el of all) {
            let txt = (el.innerText || "").trim();
            let label = (el.getAttribute("aria-label") || "").trim();

            for (let k of keywords) {
                if (txt === k || label === k || txt.includes(k)) {
                    return el.closest('div[role="button"],button') || el;
                }
            }
        }
        return null;
    }

    function findButtonFromV20_3(keywords) {
        let all = [...document.querySelectorAll('div[role="menuitem"], div[role="button"], button, span, div[role="dialog"] span, div[aria-label], div[tabindex="0"]')];
        all = all.filter(el => el.offsetParent !== null && el.offsetWidth > 0);
        for (let el of all) {
            let txt = (el.innerText || "").trim();
            let label = (el.getAttribute("aria-label") || "").trim();
            for (let k of keywords) {
                if (txt === k || label === k || txt.includes(k) || label.includes(k)) {
                    let parentBtn = el.closest('div[role="button"], button, div[role="menuitem"], div[tabindex="0"]');
                    return parentBtn ? parentBtn : el;
                }
            }
        }
        return null;
    }

    // Hàm đợi nút biến mất
    async function waitForElementToDisappear(element) {
        let maxWait = 20;
        while (maxWait > 0) {
            if (!element.isConnected || element.offsetParent === null) {
                return true;
            }
            await sleep(50);
            maxWait--;
        }
        return false;
    }

    // Đợi loading
    async function waitForGlobalLoading(statusCallback) {
        let maxWait = 80;
        let isWaiting = false;

        while (maxWait > 0) {
            let loadingIcon = document.querySelector('[role="progressbar"], img[src*="loading"], i[class*="loading"]');
            
            if (loadingIcon && loadingIcon.offsetParent !== null) {
                isWaiting = true;
                if(statusCallback) statusCallback("⏳ Loading...", "orange");
                await sleep(50);
                maxWait--;
            } else {
                if(isWaiting) await sleep(200);
                return;
            }
        }
    }

    function simulateInput(element, text) {
        element.focus();
        let lastValue = element.value;
        element.value = text;
        let event = new Event('input', { bubbles: true });
        let tracker = element._valueTracker;
        if (tracker) { tracker.setValue(lastValue); }
        element.dispatchEvent(event);
        element.dispatchEvent(new Event('change', { bubbles: true }));
    }

    // Hàm CLICK META
    async function clickMetaResult(statusEl) {
        let retry = 5;
        while (retry > 0) {
            let options = document.querySelectorAll('div[role="listbox"] span, ul[role="listbox"] span, div[role="presentation"] span');
            for (let span of options) {
                if (span.innerText.trim() === "Meta") {
                    console.log("--> Đã tìm thấy kết quả Meta! Click ngay!");
                    statusEl.innerText = "Click vào 'Meta'...";
                    span.style.border = "2px solid red";
                    safeClick(span);
                    return true;
                }
            }
            let imgs = document.querySelectorAll('div[role="listbox"] img');
            if (imgs.length > 0) {
                 console.log("--> Click vào hình ảnh kết quả đầu tiên");
                 safeClick(imgs[0]);
                 return true;
            }
            statusEl.innerText = `Đang tìm 'Meta'... (${retry})`;
            await sleep(300);
            retry--;
        }
        return false;
    }

    // Hàm CLICK MARK ZUCKERBERG
    async function clickMarkZuckerbergResult(statusEl) {
        let retry = 5;
        while (retry > 0) {
            let options = document.querySelectorAll('div[role="listbox"] span, ul[role="listbox"] span, div[role="presentation"] span');
            for (let span of options) {
                if (span.innerText.trim() === "Mark Zuckerberg") {
                    console.log("--> Đã tìm thấy Mark Zuckerberg!");
                    statusEl.innerText = "Click vào 'Mark Zuckerberg'...";
                    span.style.border = "2px solid red";
                    safeClick(span);
                    return true;
                }
            }
            let imgs = document.querySelectorAll('div[role="listbox"] img');
            if (imgs.length > 0) {
                safeClick(imgs[0]);
                return true;
            }
            statusEl.innerText = `Đang tìm Mark Zuckerberg... (${retry})`;
            await sleep(300);
            retry--;
        }
        return false;
    }

    // [ANTI-SLEEP LOGIC]
    let audioLoop = null;
    let titleInterval = null;
    const SILENT_AUDIO = 'data:audio/mp3;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjIwLjEwMAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAASW5mbwAAAA8AAAAEAAABIADAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMD//////////////////////////////////////////////////////////////////wAAADFMYXZjNTguMzUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUAIAAAAASAA8AxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAATGF2YzU4LjM1LjEwMAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAATGF2YzU4LjM1LjEwMAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAATGF2YzU4LjM1LjEwMAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAATGF2YzU4LjM1LjEwMAAAAAAAAAAAAAAA';

    function toggleAntiSleep(enable) {
        if (enable) {
            if (!audioLoop) {
                audioLoop = new Audio(SILENT_AUDIO);
                audioLoop.loop = true;
                audioLoop.volume = 0.01;
            }
            audioLoop.play().catch(e => console.log("Cần tương tác để phát nhạc ngầm"));
            let tick = false;
            if (titleInterval) clearInterval(titleInterval);
            titleInterval = setInterval(() => {
                document.title = tick ? "⚡ Auto Dame FB TheGioiios..." : "🛡️ Auto Dame FB TheGioiiOS";
                tick = !tick;
            }, 2000);
        } else {
            if (audioLoop) audioLoop.pause();
            if (titleInterval) {
                clearInterval(titleInterval);
                document.title = "Facebook";
            }
        }
    }

    // ==========================================
    // UI CONTROL
    // ==========================================
    let isPaused = false;
    let shouldStop = false;
    let isMini = false;
    let posX = 20, posY = 80;
    let isDragging = false;
    let dragOffsetX, dragOffsetY;

    const panel = document.createElement("div");
    panel.id = "autoDameFB";
    
    const fullStyle = {
        position: "fixed",
        top: posY + "px",
        left: posX + "px",
        width: "300px",
        background: "linear-gradient(145deg, #1a1a2e 0%, #16213e 100%)",
        color: "#fff",
        padding: "0",
        borderRadius: "16px",
        zIndex: 999999,
        border: "1px solid rgba(0, 255, 255, 0.3)",
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        fontSize: "13px",
        boxShadow: "0 20px 40px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(0, 255, 255, 0.2) inset, 0 0 20px rgba(0, 255, 255, 0.2)",
        backdropFilter: "blur(10px)",
        transition: "box-shadow 0.3s ease",
        cursor: "default",
        userSelect: "none"
    };
    Object.assign(panel.style, fullStyle);

    function makeDraggable(element) {
        const header = element.querySelector('.drag-handle');
        if (!header) return;
        
        header.addEventListener('mousedown', (e) => {
            if (e.target.closest('button')) return;
            isDragging = true;
            dragOffsetX = e.clientX - element.offsetLeft;
            dragOffsetY = e.clientY - element.offsetTop;
            element.style.transition = 'none';
            element.style.cursor = 'grabbing';
            element.style.opacity = '0.95';
            e.preventDefault();
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            
            let newX = e.clientX - dragOffsetX;
            let newY = e.clientY - dragOffsetY;
            
            newX = Math.max(0, Math.min(window.innerWidth - element.offsetWidth, newX));
            newY = Math.max(0, Math.min(window.innerHeight - element.offsetHeight, newY));
            
            element.style.left = newX + 'px';
            element.style.top = newY + 'px';
            
            posX = newX;
            posY = newY;
        });

        document.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                element.style.transition = 'box-shadow 0.3s ease';
                element.style.cursor = 'default';
                element.style.opacity = '1';
            }
        });
    }

    const renderPanel = () => {
        if (isMini) {
            panel.innerHTML = `
                <div class="drag-handle" style="cursor: move; padding: 8px; background: linear-gradient(145deg, #0f3460, #1a1a2e); border-radius: 16px 16px 0 0; border-bottom: 1px solid #00ffff33;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:18px; filter: drop-shadow(0 0 5px cyan);">⚡</span>
                        <div style="flex:1; background: rgba(255,255,255,0.1); height:6px; border-radius:3px; overflow:hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.5);">
                            <div id="miniBar" style="width:0%; height:100%; background: linear-gradient(90deg, #00ffff, #ff00ff); border-radius:3px;"></div>
                        </div>
                        <button id="btnExpand" style="background: rgba(255,255,255,0.1); border:1px solid #00ffff; color:#00ffff; cursor:pointer; border-radius:50%; width:24px; height:24px; display:flex; align-items:center; justify-content:center; font-size:16px; transition: all 0.2s;">➕</button>
                    </div>
                </div>
                <div style="padding:8px; background: rgba(0,0,0,0.3);">
                    <div id="miniStt" style="font-size:11px; color:#00ffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; text-shadow: 0 0 5px cyan;">Auto Dame FB Trần Tuấn</div>
                </div>
            `;
            panel.style.width = "200px";
            panel.style.background = "linear-gradient(145deg, #0f172a, #1e293b)";
            
            const bar = panel.querySelector("#miniBar");
            const stt = panel.querySelector("#miniStt");
            const btnExpand = panel.querySelector("#btnExpand");
            
            btnExpand.onclick = () => {
                isMini = false;
                renderPanel();
                makeDraggable(panel);
            };
            
            return { bar, stt };
        } else {
            panel.innerHTML = `
                <div class="drag-handle" style="cursor: move; padding: 15px 20px; background: linear-gradient(145deg, #0f3460, #1a1a2e); border-radius: 16px 16px 0 0; border-bottom: 2px solid #00ffff; display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 24px; filter: drop-shadow(0 0 8px cyan);">⚡</span>
                        <div>
                            <h3 style="margin:0; color: #fff; font-weight: 600; font-size: 16px; letter-spacing: 0.5px; text-shadow: 0 0 10px rgba(0,255,255,0.5);">Auto Dame FB Trần Tuấn</h3>
                            <div style="font-size: 11px; color: #00ffff; opacity: 0.8;">TURBO 0.9s • 65 bước</div>
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button id="btnMinimize" style="background: rgba(255,255,255,0.1); border:1px solid #00ffff80; color:#00ffff; cursor:pointer; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-size:18px; transition: all 0.2s;">−</button>
                    </div>
                </div>
                
                <div style="padding: 20px;">
                    <div style="margin-bottom: 20px; display: flex; gap: 12px;">
                        <div style="flex:1;">
                            <label style="display: block; margin-bottom: 6px; color: #00ffff; font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">🔁 Số vòng</label>
                            <input id="inpMaxLoop" type="number" value="1" style="width:100%; padding: 10px; background: rgba(0,0,0,0.3); border: 1px solid #00ffff40; border-radius: 10px; color: #fff; font-size: 14px; outline: none; transition: all 0.2s;" onmouseover="this.style.borderColor='#00ffff'" onmouseout="this.style.borderColor='#00ffff40'">
                        </div>
                        <div style="flex:1;">
                            <label style="display: block; margin-bottom: 6px; color: #00ffff; font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">⏱️ Nghỉ (phút)</label>
                            <input id="inpDelayMin" type="number" value="0" style="width:100%; padding: 10px; background: rgba(0,0,0,0.3); border: 1px solid #00ffff40; border-radius: 10px; color: #fff; font-size: 14px; outline: none; transition: all 0.2s;" onmouseover="this.style.borderColor='#00ffff'" onmouseout="this.style.borderColor='#00ffff40'">
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 20px; background: rgba(0,0,0,0.2); border-radius: 12px; padding: 12px;">
                        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer;">
                            <input type="checkbox" id="chkAntiSleep" checked style="width: 18px; height: 18px; accent-color: #00ffff;">
                            <span style="color: #fff; font-size: 13px;">📌 Ghim tab / Chống ngủ</span>
                        </label>
                    </div>
                    
                    <div style="margin-bottom: 15px; background: rgba(0,0,0,0.2); border-radius: 12px; padding: 12px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                            <span style="color: #00ffff; font-size: 12px;">TRẠNG THÁI</span>
                            <span id="stt" style="color: #ffff00; font-weight: 600; font-size: 12px;">Sẵn sàng (0.9s)</span>
                        </div>
                        <div style="background: rgba(0,0,0,0.3); height: 8px; border-radius: 4px; overflow: hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.5);">
                            <div id="progressBar" style="width:0%; height:100%; background: linear-gradient(90deg, #00ffff, #ff00ff); border-radius: 4px; transition: width 0.3s ease;"></div>
                        </div>
                    </div>
                    
                    <div style="display: flex; gap: 10px;">
                        <button id="btnStart" style="flex:2; padding: 12px; background: linear-gradient(145deg, #00c853, #00e676); border: none; border-radius: 12px; color: white; font-weight: 700; font-size: 14px; cursor: pointer; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 5px 15px rgba(0,230,118,0.3); transition: all 0.2s;">🚀 CHẠY</button>
                        <button id="btnPause" style="flex:1; padding: 12px; background: linear-gradient(145deg, #ff9800, #ffb74d); border: none; border-radius: 12px; color: white; font-weight: 700; font-size: 14px; cursor: pointer; display: none; transition: all 0.2s;">⏸️</button>
                        <button id="btnStop" style="flex:1; padding: 12px; background: linear-gradient(145deg, #f44336, #ff7043); border: none; border-radius: 12px; color: white; font-weight: 700; font-size: 14px; cursor: pointer; display: none; transition: all 0.2s;">⏹️</button>
                    </div>
                    
                    <div id="btnResume" style="display:none; margin-top: 10px;">
                        <button style="width:100%; padding: 12px; background: linear-gradient(145deg, #2196f3, #64b5f6); border: none; border-radius: 12px; color: white; font-weight: 700; font-size: 14px; cursor: pointer; text-transform: uppercase; letter-spacing: 1px;">▶️ TIẾP TỤC</button>
                    </div>
                    
                    <div style="margin-top: 15px; text-align: center; font-size: 10px; color: #00ffff60; letter-spacing: 0.5px;">
                        © Trần Tuấn • Premium Edition • v13.2
                    </div>
                </div>
            `;
            
            panel.style.width = "300px";
            panel.style.background = "linear-gradient(145deg, #0f172a, #1e293b)";
            
            const btnMinimize = panel.querySelector("#btnMinimize");
            btnMinimize.onclick = () => {
                isMini = true;
                renderPanel();
                makeDraggable(panel);
            };
            
            bindMainEvents();
            
            return {
                stt: panel.querySelector("#stt"),
                bar: panel.querySelector("#progressBar")
            };
        }
    };
    
    document.body.appendChild(panel);
    renderPanel();
    makeDraggable(panel);
    
    function bindMainEvents() {
        if(isMini) return;
        
        const btnStart = panel.querySelector("#btnStart");
        const btnPause = panel.querySelector("#btnPause");
        const btnStop = panel.querySelector("#btnStop");
        const btnResumeDiv = panel.querySelector("#btnResume");
        const btnResume = btnResumeDiv?.querySelector("button");
        const chkAntiSleep = panel.querySelector("#chkAntiSleep");

        if (btnStart) {
            btnStart.onclick = startProcess;
            btnStart.onmouseover = () => { btnStart.style.transform = 'translateY(-2px)'; };
            btnStart.onmouseout = () => { btnStart.style.transform = 'translateY(0)'; };
        }
        
        if (btnPause) {
            btnPause.onclick = () => { isPaused = true; updateUIState(); };
            btnPause.onmouseover = () => { btnPause.style.transform = 'translateY(-2px)'; };
            btnPause.onmouseout = () => { btnPause.style.transform = 'translateY(0)'; };
        }
        
        if (btnResume) {
            btnResume.onclick = () => { isPaused = false; updateUIState(); };
            btnResume.onmouseover = () => { btnResume.style.transform = 'translateY(-2px)'; };
            btnResume.onmouseout = () => { btnResume.style.transform = 'translateY(0)'; };
        }
        
        if (btnStop) {
            btnStop.onclick = () => {
                if(confirm("DỪNG hoàn toàn?")) {
                    shouldStop = true;
                    isPaused = false;
                    toggleAntiSleep(false);
                    updateStatus("Đang dừng...", "red");
                }
            };
            btnStop.onmouseover = () => { btnStop.style.transform = 'translateY(-2px)'; };
            btnStop.onmouseout = () => { btnStop.style.transform = 'translateY(0)'; };
        }
    }

    function updateUIState() {
        if(isMini) return;
        
        const btnStart = panel.querySelector("#btnStart");
        const btnPause = panel.querySelector("#btnPause");
        const btnStop = panel.querySelector("#btnStop");
        const btnResumeDiv = panel.querySelector("#btnResume");
        
        if (!btnStart) return;
        
        if (audioLoop && !audioLoop.paused) {
            btnStart.style.display = "none";
            btnStop.style.display = "block";
            if (isPaused) {
                btnPause.style.display = "none";
                btnResumeDiv.style.display = "block";
            } else {
                btnPause.style.display = "block";
                btnResumeDiv.style.display = "none";
            }
        } else {
            btnStart.style.display = "block";
            btnPause.style.display = "none";
            btnStop.style.display = "none";
            btnResumeDiv.style.display = "none";
        }
    }

    function updateStatus(text, color = "yellow") {
        if (isMini) {
            const el = panel.querySelector("#miniStt");
            if (el) {
                el.innerText = text;
                el.style.color = color;
                el.style.textShadow = `0 0 5px ${color}`;
            }
        } else {
            const el = panel.querySelector("#stt");
            if (el) {
                el.innerText = text;
                el.style.color = color;
            }
        }
    }
    
    function updateProgress(percent) {
        if (isMini) {
            const el = panel.querySelector("#miniBar");
            if (el) el.style.width = percent + "%";
        } else {
            const el = panel.querySelector("#progressBar");
            if (el) el.style.width = percent + "%";
        }
    }

    // --- MAIN PROCESS (ĐÃ THÊM KIỂM TRA LỖI HIỂN THỊ) ---
    async function startProcess() {
        // 🛡️ KIỂM TRA LỖI HIỂN THỊ TRƯỚC KHI CHẠY
        const fixed = await checkAndFixDisplay();
        if (fixed) return; // Nếu đã refresh thì dừng lại
        
        let maxLoops = 1, delayMinutes = 0, useAntiSleep = true;
        if (!isMini) {
            maxLoops = parseInt(panel.querySelector("#inpMaxLoop").value) || 1;
            delayMinutes = parseInt(panel.querySelector("#inpDelayMin").value) || 0;
            useAntiSleep = panel.querySelector("#chkAntiSleep").checked;
        }

        let currentLoop = 0;
        shouldStop = false;
        isPaused = false;

        if (useAntiSleep) toggleAntiSleep(true);
        updateUIState();

        while (currentLoop < maxLoops && !shouldStop) {
            currentLoop++;
            console.log(`%c[LOOP] Vòng ${currentLoop}/${maxLoops} - Auto Dame FB Trần Tuấn`, "color: cyan; font-size: 14px;");

            for (let i = 0; i < steps.length; i++) {
                // 🛡️ KIỂM TRA LỖI HIỂN THỊ TRONG KHI CHẠY
                if (document.body.innerText.includes('下载')) {
                    await checkAndFixDisplay();
                    return;
                }
                
                if (shouldStop) break;
                while (isPaused) { await sleep(200); if (shouldStop) break; }

                let step = steps[i];
                updateStatus(`[Vòng ${currentLoop}] ${step.name}`, "yellow");
                updateProgress((step.step / 65) * 100);

                // Xử lý CLICK_META_RESULT
                if (step.specialAction === "CLICK_META_RESULT") {
                    let dummyStt = { innerText: "" };
                    let success = await clickMetaResult(dummyStt);
                    updateStatus(dummyStt.innerText || "Chọn Meta...", "orange");
                    if (!success) {
                        let inputEl = getElementByXpath(INPUT_XPATH);
                        if(inputEl) inputEl.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', keyCode: 13, bubbles: true}));
                    }
                    await waitForGlobalLoading(updateStatus);
                    await sleep(SHORT_DELAY);
                    continue;
                }
                
                // Xử lý CLICK_MARK_ZUCKERBERG_RESULT
                if (step.specialAction === "CLICK_MARK_ZUCKERBERG_RESULT") {
                    let dummyStt = { innerText: "" };
                    let success = await clickMarkZuckerbergResult(dummyStt);
                    updateStatus(dummyStt.innerText || "Chọn Mark Zuckerberg...", "orange");
                    if (!success) {
                        let inputEl = getElementByXpath(INPUT_XPATH);
                        if(inputEl)
                        inputEl.dispatchEvent(
                        new KeyboardEvent('keydown',
                        {key: 'Enter', keyCode: 13, bubbles: true}));
                    }
                    await waitForGlobalLoading(updateStatus);
                    await sleep(SHORT_DELAY);
                    continue;
                }

                let el = null;
                for(let retry=0; retry<5; retry++){
                    if (shouldStop) break;
                    if (step.xpath) el = getElementByXpath(step.xpath);
                    if (!el) {
                        if (step.name === "Next")
                            el = findButtonInsideDialog(["Next", "Tiếp", "Tiếp tục"]);
                        else if (step.name === "Submit")
                            el = findButtonInsideDialog(["Submit", "Gửi", "Send"]);
                        else if (step.name === "Done")
                            el = findButtonInsideDialog(["Done", "Xong", "Hoàn tất", "Đóng", "Close"]);
                        else
                            el = findButtonFromV20_3([step.name]);
                    }
                    if(el) break;
                    await sleep(300);
                }

                if (shouldStop) break;

                if (el) {
                    if (step.inputData) {
                        el.style.border = "2px solid yellow";
                        simulateInput(el, step.inputData);
                        updateStatus("Chờ load...", "orange");
                        await sleep(INPUT_DELAY);
                    } else {
                        el.style.border = "2px solid #00ff00";
                        safeClick(el);
                        
                        if (step.name === "Next" || step.name === "Submit") {
                            updateStatus("Đợi nút ẩn...", "cyan");
                            await waitForElementToDisappear(el);
                        }
                        
                        await waitForGlobalLoading(updateStatus);
                        
                        updateStatus(`Nghỉ 0.9s...`, "#888");
                        await sleep(DELAY_TIME);
                    }
                } else {
                    // Không dừng hẳn, chỉ bỏ qua bước
                    console.log(`⚠️ Bỏ qua bước ${step.step}: ${step.name}`);
                }
            }

            if (shouldStop) break;

            if (currentLoop < maxLoops) {
                if (delayMinutes > 0) {
                    let secondsLeft = delayMinutes * 60;
                    while (secondsLeft > 0 && !shouldStop) {
                        updateStatus(`Nghỉ: ${secondsLeft}s...`, "#00BFFF");
                        await sleep(1000);
                        secondsLeft--;
                    }
                } else await sleep(SHORT_DELAY);
            }
        }

        if (!shouldStop) {
            updateStatus("✅ HOÀN THÀNH!", "#00ff88");
            updateProgress(100);
            alert(`Đã chạy xong ${currentLoop} vòng với tốc độ 0.9s!`);
        }
        
        toggleAntiSleep(false);
        updateUIState();
    };
})();
         // Cre : Https://t.me/@thegioiios

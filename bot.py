const { TelegramClient, Api } = require("telegram");
const { StringSession } = require("telegram/sessions");
const mongoose = require("mongoose");
const puppeteer = require("puppeteer");

// --- [ CONFIGURATION ] ---
const apiId = 21552435;
const apiHash = "5b108bd2fdd31c0c34bc65f24a5216a0";
const botToken = "8464390807:AAGVxObZ60Se34Kjo3nX34I0iDa8VBAcsRY";
const OWNER_ID = "6632236983";
const MONGO_URL = "mongodb+srv://Elevenyts:Elevenyts@cluster0.vuyc1u2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

// --- [ DB SETUP ] ---
mongoose.connect(MONGO_URL);
const User = mongoose.model("User", { userId: String, auth: Boolean });

const client = new TelegramClient(new StringSession(""), apiId, apiHash, { connectionRetries: 5 });

(async () => {
    await client.start({ botAuthToken: botToken });
    console.log("🚀 AHMED X STOREZ: NODE.JS LIVE");

    const BR = "━━━━━━━━━━━━━━━━━━━━━━━━";

    client.addEventHandler(async (event) => {
        const message = event.message;
        if (!message || !message.text) return;

        const senderId = message.senderId.toString();
        const text = message.text.toUpperCase();

        // --- [ START COMMAND ] ---
        if (text.startsWith("/START")) {
            const isOwner = senderId === OWNER_ID;
            const isAuth = await User.findOne({ userId: senderId });
            const STATUS = (isOwner || isAuth) ? "✅ ⚡ AUTHORIZED ⚡" : "❌ ⚡ ACCESS DENIED ⚡";

            await client.sendMessage(message.chatId, {
                message: `${BR}\n🔥 **WELCOME TO AHMED X STOREZ**\n${BR}\n👤 **USER ID:** ${senderId}\n🛡 **STATUS:** ${STATUS}\n🌐 **ENGINE:** NODE.JS V20\n${BR}\n✨ **PREMIUM SETUP X ACTIVE**\n${BR}`,
                parseMode: "markdown"
            });
        }

        // --- [ ADMIN: ADD USER ] ---
        if (text.startsWith("/ADD") && senderId === OWNER_ID) {
            const targetId = text.split(" ")[1];
            await User.findOneAndUpdate({ userId: targetId }, { auth: true }, { upsert: true });
            await client.sendMessage(message.chatId, { message: `${BR}\n✅ **USER ${targetId} AUTHORIZED**\n${BR}` });
        }

        // --- [ ADMIN: REMOVE USER ] ---
        if (text.startsWith("/REMOVE") && senderId === OWNER_ID) {
            const targetId = text.split(" ")[1];
            await User.deleteOne({ userId: targetId });
            await client.sendMessage(message.chatId, { message: `${BR}\n➖ **USER ${targetId} ACCESS TERMINATED**\n${BR}` });
        }

        // --- [ INDOFIX ENGINE ] ---
        if (text.startsWith("/INDOFIX")) {
            const isOwner = senderId === OWNER_ID;
            const isAuth = await User.findOne({ userId: senderId });
            if (!isOwner && !isAuth) return client.sendMessage(message.chatId, { message: "❌ NO ACCESS" });

            const args = message.text.split(" ");
            if (args.length < 3) return client.sendMessage(message.chatId, { message: "📝 USE: /INDOFIX USER PASS" });

            const statusMsg = await client.sendMessage(message.chatId, { message: `${BR}\n⚙️ **NODE ENGINE: PROCESSING...**\n${BR}` });

            try {
                const browser = await puppeteer.launch({ args: ["--no-sandbox", "--disable-setuid-sandbox"] });
                const page = await browser.newPage();
                await page.goto("https://business.facebook.com/business/loginpage/");
                await page.type('input[name="email"]', args[1]);
                await page.type('input[name="pass"]', args[2]);
                await page.click('button[name="login"]');
                await new Promise(r => setTimeout(r, 10000));
                await browser.close();
                await client.editMessage(message.chatId, { message: statusMsg.id, text: `${BR}\n✅ **INDO FIX SUCCESS BY AHMED X**\n${BR}` });
            } catch (e) {
                await client.editMessage(message.chatId, { message: statusMsg.id, text: `❌ ERROR: ${e.message.toUpperCase()}` });
            }
        }
    });
})();

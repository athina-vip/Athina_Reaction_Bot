<?php
/**
 * Auto Reaction Bot - Enhanced Version
 * Built for Render/Railway Deployment
 */

// --- CONFIGURATION ---
// Token များကို ဒီနေရာတွင် တိုက်ရိုက်ထည့်ထားပေးသည် (Render Env မှာ မထည့်တတ်ပါက ဤနေရာတွင် အလုပ်လုပ်မည်)
$BOT_TOKEN = '8250583948:AAEEcsNCDtW4Wczo_nsv7oQrZzqZdikqhMo';
$BOT_USERNAME = 'Athina_Reaction_Bot';

// Reaction ၅၀ ကျော် ရအောင် Emoji list ကို အစုံထည့်ပေးထားသည်
$EMOJI_LIST = '👍❤🔥🥰👏😁🎉🤩🙏👌🕊😍🐳❤‍🔥💯⚡🏆😇🤣😂🌚🔥✨🎈💎🆒🆙🆗🆒🌹🌷🌺💐🌸🌿🍓🍎🍒🍑🍊🍍🚀✈🛸🛰🚁🛶🚢🏎🏍🌈🌞⭐🌙⚡🔥💧💦💤✨💫';

$RANDOM_LEVEL = 0; // 0 ဆိုလျှင် မက်ဆေ့တိုင်းကို Reaction ပေးမည်
$RESTRICTED_CHATS = '';

// --- CONSTANTS ---
const START_MESSAGE = '👋 Hello there! Welcome to *Athina Auto Reaction Bot* 🎉';
const DONATE_MESSAGE = '🙏 Support us to keep the bot alive!';

/**
 * Telegram Bot API Class
 */
class TelegramBotAPI {
    private $apiUrl;
    public function __construct($botToken) {
        $this->apiUrl = "https://api.telegram.org/bot{$botToken}/";
    }
    
    private function callApi($action, $body) {
        $url = $this->apiUrl . $action;
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
        curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        $response = curl_exec($ch);
        curl_close($ch);
        return json_decode($response, true);
    }
    
    public function setMessageReaction($chatId, $messageId, $emoji) {
        return $this->callApi('setMessageReaction', [
            'chat_id' => $chatId,
            'message_id' => $messageId,
            'reaction' => [['type' => 'emoji', 'emoji' => $emoji]],
            'is_big' => true
        ]);
    }

    public function sendMessage($chatId, $text) {
        $this->callApi('sendMessage', [
            'chat_id' => $chatId,
            'text' => $text,
            'parse_mode' => 'Markdown'
        ]);
    }
}

// --- HELPER FUNCTIONS ---
function splitEmojis($emojiString) {
    preg_match_all('/[\x{1F600}-\x{1F64F}]|[\x{1F300}-\x{1F5FF}]|[\x{1F680}-\x{1F6FF}]|[\x{1F1E0}-\x{1F1FF}]|[\x{2600}-\x{26FF}]|[\x{2700}-\x{27BF}]|[\x{1F900}-\x{1F9FF}]/u', $emojiString, $matches);
    return $matches[0];
}

// --- MAIN EXECUTION ---
try {
    $reactions = splitEmojis($EMOJI_LIST);
    $botApi = new TelegramBotAPI($BOT_TOKEN);
    
    // POST Request (Webhook မှလာသော data) ကို လက်ခံခြင်း
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);
    
    if ($data) {
        $content = $data['message'] ?? $data['channel_post'] ?? null;
        if ($content) {
            $chatId = $content['chat']['id'];
            $messageId = $content['message_id'];
            $text = $content['text'] ?? '';

            if ($text === '/start') {
                $botApi->sendMessage($chatId, START_MESSAGE);
            } else {
                // Emoji စာရင်းထဲမှ တစ်ခုကို ကျပန်းရွေးပြီး Reaction ပေးခြင်း
                $randomEmoji = $reactions[array_rand($reactions)];
                $botApi->setMessageReaction($chatId, $messageId, $randomEmoji);
            }
        }
    }

    // Health Check အတွက် GET request လက်ခံခြင်း
    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
        echo "Bot is running perfectly! Emojis loaded: " . count($reactions);
    }

} catch (Exception $e) {
    http_response_code(200);
    echo "Ok";
}

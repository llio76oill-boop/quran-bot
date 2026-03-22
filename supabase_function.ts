import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const TELEGRAM_TOKEN = Deno.env.get("TELEGRAM_TOKEN");
const CHANNEL_ID = Deno.env.get("CHANNEL_ID");
const QURAN_API_URL = "https://api.alquran.cloud/v1";

// قاموس أسماء السور بالعربية
const SURAH_NAMES: Record<number, string> = {
  1: "الفاتحة", 2: "البقرة", 3: "آل عمران", 4: "النساء", 5: "المائدة",
  6: "الأنعام", 7: "الأعراف", 8: "الأنفال", 9: "التوبة", 10: "يونس",
  11: "هود", 12: "يوسف", 13: "الرعد", 14: "إبراهيم", 15: "الحجر",
  16: "النحل", 17: "الإسراء", 18: "الكهف", 19: "مريم", 20: "طه",
  21: "الأنبياء", 22: "الحج", 23: "المؤمنون", 24: "النور", 25: "الفرقان",
  26: "الشعراء", 27: "النمل", 28: "القصص", 29: "العنكبوت", 30: "الروم",
  31: "لقمان", 32: "السجدة", 33: "الأحزاب", 34: "سبأ", 35: "فاطر",
  36: "يس", 37: "الصافات", 38: "ص", 39: "الزمر", 40: "غافر",
  41: "فصلت", 42: "الشورى", 43: "الزخرف", 44: "الدخان", 45: "الجاثية",
  46: "الأحقاف", 47: "محمد", 48: "الفتح", 49: "الحجرات", 50: "ق",
  51: "الذاريات", 52: "الطور", 53: "النجم", 54: "القمر", 55: "الرحمن",
  56: "الواقعة", 57: "الحديد", 58: "المجادلة", 59: "الحشر", 60: "الممتحنة",
  61: "الصف", 62: "الجمعة", 63: "المنافقون", 64: "التغابن", 65: "الطلاق",
  66: "التحريم", 67: "الملك", 68: "القلم", 69: "الحاقة", 70: "المعارج",
  71: "نوح", 72: "الجن", 73: "المزمل", 74: "المدثر", 75: "القيامة",
  76: "الإنسان", 77: "المرسلات", 78: "النبأ", 79: "النازعات", 80: "عبس",
  81: "التكوير", 82: "الإنفطار", 83: "المطففين", 84: "الانشقاق", 85: "البروج",
  86: "الطارق", 87: "الأعلى", 88: "الغاشية", 89: "الفجر", 90: "البلد",
  91: "الشمس", 92: "الليل", 93: "الضحى", 94: "الشرح", 95: "التين",
  96: "العلق", 97: "القدر", 98: "البينة", 99: "الزلزلة", 100: "العاديات",
  101: "القارعة", 102: "التكاثر", 103: "العصر", 104: "الهمزة", 105: "الفيل",
  106: "قريش", 107: "الماعون", 108: "الكوثر", 109: "الكافرون", 110: "النصر",
  111: "المسد", 112: "الإخلاص", 113: "الفلق", 114: "الناس"
};

async function getRandomVerse() {
  try {
    const surahNum = Math.floor(Math.random() * 114) + 1;
    
    const response = await fetch(`${QURAN_API_URL}/surah/${surahNum}`);
    const data = await response.json();
    
    if (data.code !== 200 || !data.data) {
      throw new Error("Failed to fetch surah");
    }
    
    const ayahs = data.data.ayahs || [];
    if (ayahs.length === 0) {
      throw new Error("No ayahs found");
    }
    
    const verse = ayahs[Math.floor(Math.random() * ayahs.length)];
    
    return {
      text: verse.text.trim(),
      surah_num: surahNum,
      surah_name: SURAH_NAMES[surahNum] || `السورة ${surahNum}`,
      verse_num: verse.numberInSurah
    };
  } catch (error) {
    console.error("Error fetching verse:", error);
    return null;
  }
}

function formatVerseMessage(verse: any): string {
  const cleaned_text = verse.text.trim();
  const formatted_verse = `﴿${cleaned_text}﴾`;
  const surah_info = `${verse.surah_name} - الآية ${verse.verse_num}`;
  
  return `${formatted_verse}\n\n📖 ${surah_info}\n\n🕌 @aya_Quraan1`;
}

async function sendMessage(text: string) {
  try {
    const url = `https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`;
    
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        chat_id: CHANNEL_ID,
        text: text,
        parse_mode: "HTML"
      })
    });
    
    const result = await response.json();
    
    if (result.ok) {
      console.log("✅ تم إرسال الآية بنجاح");
      return true;
    } else {
      console.error("❌ فشل الإرسال:", result);
      return false;
    }
  } catch (error) {
    console.error("❌ خطأ في الإرسال:", error);
    return false;
  }
}

serve(async (req) => {
  try {
    console.log("🕌 بدء إرسال الآية...");
    
    const verse = await getRandomVerse();
    
    if (!verse) {
      return new Response(
        JSON.stringify({ error: "Failed to get verse" }),
        { status: 500, headers: { "Content-Type": "application/json" } }
      );
    }
    
    const message = formatVerseMessage(verse);
    const sent = await sendMessage(message);
    
    if (sent) {
      return new Response(
        JSON.stringify({ 
          success: true, 
          verse: verse.surah_name,
          message: "✅ تم إرسال الآية بنجاح"
        }),
        { status: 200, headers: { "Content-Type": "application/json" } }
      );
    } else {
      return new Response(
        JSON.stringify({ error: "Failed to send message" }),
        { status: 500, headers: { "Content-Type": "application/json" } }
      );
    }
  } catch (error) {
    console.error("❌ خطأ:", error);
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
});

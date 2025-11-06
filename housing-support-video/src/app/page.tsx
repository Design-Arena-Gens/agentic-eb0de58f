export default function Home() {
  return (
    <div className="bg-slate-100">
      <main className="mx-auto flex min-h-screen max-w-6xl flex-col gap-16 px-6 pb-24 pt-24 sm:px-10 lg:px-16">
        <section className="rounded-3xl bg-white p-8 shadow-sm ring-1 ring-slate-200 md:p-12">
          <div className="grid gap-10 lg:grid-cols-[3fr_4fr] lg:items-center">
            <div className="space-y-6">
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">
                राष्ट्रीय आवास सहायता कार्यक्रम
              </p>
              <h1 className="text-4xl font-semibold leading-tight text-slate-900 md:text-5xl">
                सुरक्षित घर की दिशा में भरोसेमंद सरकारी पहल
              </h1>
              <p className="text-lg leading-relaxed text-slate-600">
                यह 60 सेकंड का हिंदी वीडियो कार्यक्रम के उद्देश्य, पात्रता, ऑनलाइन
                आवेदन प्रक्रिया और मूल लाभों को शांतिपूर्ण प्रस्तुति, स्पष्ट
                वॉयसओवर और हल्के संगीत के साथ समझाता है।
              </p>
              <dl className="grid gap-4 text-base text-slate-700 sm:grid-cols-2">
                <div className="rounded-2xl border border-slate-200 p-4">
                  <dt className="text-sm font-semibold text-slate-500">
                    अवधि
                  </dt>
                  <dd className="text-lg font-semibold text-slate-900">
                    60 सेकंड
                  </dd>
                </div>
                <div className="rounded-2xl border border-slate-200 p-4">
                  <dt className="text-sm font-semibold text-slate-500">
                    भाषा
                  </dt>
                  <dd className="text-lg font-semibold text-slate-900">
                    हिंदी (तटस्थ, जानकारीपूर्ण शैली)
                  </dd>
                </div>
              </dl>
            </div>
            <div className="overflow-hidden rounded-3xl border border-slate-200 bg-slate-900">
              <video
                className="h-full w-full object-cover"
                controls
                preload="metadata"
                poster="/posters/housing-support.jpg"
              >
                <source
                  src="/videos/housing-support.mp4"
                  type="video/mp4"
                />
                आपका ब्राउज़र वीडियो टैग को सपोर्ट नहीं करता।
              </video>
            </div>
          </div>
        </section>

        <section className="grid gap-8 rounded-3xl bg-white p-10 shadow-sm ring-1 ring-slate-200 md:grid-cols-2">
          <article className="space-y-5">
            <h2 className="text-2xl font-semibold text-slate-900">
              स्क्रीन पर मुख्य बिंदु
            </h2>
            <ul className="space-y-4 text-base leading-relaxed text-slate-700">
              <li className="flex gap-3">
                <span className="mt-2 h-2 w-2 rounded-full bg-blue-500"></span>
                <span>
                  कार्यक्रम का परिचय: सुरक्षित और किफायती आवास उपलब्ध कराने
                  वाली राष्ट्रीय योजना।
                </span>
              </li>
              <li className="flex gap-3">
                <span className="mt-2 h-2 w-2 rounded-full bg-amber-500"></span>
                <span>
                  पात्रता: जिन परिवारों की आय निर्धारित सीमा में है और जिनके
                  पास स्थायी घर नहीं है।
                </span>
              </li>
              <li className="flex gap-3">
                <span className="mt-2 h-2 w-2 rounded-full bg-emerald-500"></span>
                <span>
                  ऑनलाइन आवेदन प्रक्रिया: पोर्टल पर पंजीकरण, विवरण भरना और डिजिटल
                  दस्तावेज़ अपलोड करना।
                </span>
              </li>
              <li className="flex gap-3">
                <span className="mt-2 h-2 w-2 rounded-full bg-violet-500"></span>
                <span>
                  प्रमुख लाभ: घर खरीद, निर्माण या सुधार के लिए सीधे खाते में
                  वित्तीय सहायता और पारदर्शी प्रक्रिया।
                </span>
              </li>
            </ul>
          </article>

          <article className="space-y-6 rounded-2xl bg-slate-50 p-6">
            <h3 className="text-xl font-semibold text-slate-900">
              उपयोग करने का तरीका
            </h3>
            <div className="space-y-4 text-sm leading-7 text-slate-700">
              <p>
                ऊपर दिए गए वीडियो को प्ले करें और संपूर्ण ऑडियो-विज़ुअल मार्गदर्शिका
                का उपयोग अधिकारियों या अर्ज़ी प्रक्रिया से पहले ट्रस्ट-बिल्डिंग
                जानकारी के लिए करें।
              </p>
              <p>
                वीडियो में शांत बैकग्राउंड संगीत, स्पष्ट हिंदी वॉयसओवर और सरल
                दृश्य शामिल हैं जो दस्तावेज़, घर तथा ऑनलाइन आवेदन को प्रदर्शित
                करते हैं।
              </p>
              <p>
                आवश्यकता पड़ने पर वीडियो को डाउनलोड करने के लिए प्लेयर मेन्यू का
                उपयोग करें और क्लाइंट, नागरिक या प्रशिक्षण टीम के साथ साझा करें।
              </p>
            </div>
          </article>
        </section>
      </main>
    </div>
  );
}

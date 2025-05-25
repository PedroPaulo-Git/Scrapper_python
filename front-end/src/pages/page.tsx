"use client";

import React, { useState, useEffect } from "react";
// import Image from "next/image";
import { RiErrorWarningLine } from "react-icons/ri";

const Congratulations = () => {
useEffect(() => {
  if (typeof window !== "undefined" && window.fbq && !localStorage.getItem("purchase_tracked")) {
    window.fbq("track", "Purchase", {
      value: 37.90,
      currency: "USD",
    });
    localStorage.setItem("purchase_tracked", "true");
    console.log("✅ Evento de compra enviado");
  }
}, []);

  const [username, setUsername] = useState("");

  useEffect(() => {
    const savedUsername = localStorage.getItem("target_username");
    if (savedUsername) setUsername(savedUsername);
  }, []);

  //const [currentTime, setCurrentTime] = useState(new Date()); // Hora atual
  const [timeLeft, setTimeLeft] = useState({
    hours: 0,
    minutes: 10,
    seconds: 0,
  });
  const [showError429, setShowError429] = useState(false);
  const [vagasData, setVagasData] = useState("");
  useEffect(() => {
    // Função para atualizar o tempo restante
    const calculateTimeLeft = () => {
      setTimeLeft((prevTime) => {
        let { hours, minutes, seconds } = prevTime;

        // Subtrai 1 segundo
        if (seconds > 0) {
          seconds -= 1;
        } else if (minutes > 0) {
          minutes -= 1;
          seconds = 59;
        } else if (hours > 0) {
          hours -= 1;
          minutes = 59;
          seconds = 59;
        }

        return { hours, minutes, seconds };
      });
    };

    // Atualiza a data no formato dd/mm/yyyy
    const today = new Date();
    const day = today.getDate().toString().padStart(2, "0");
    const month = (today.getMonth() + 1).toString().padStart(2, "0");
    const year = today.getFullYear();
    const formattedDate = `${day}/${month}/${year}`;
    setVagasData(formattedDate);

    // Define o intervalo para o cálculo do tempo restante a cada segundo
    const interval = setInterval(() => {
      // Chama o cálculo do tempo restante
      calculateTimeLeft();

      // Verifica se o tempo chegou a 0
      if (
        timeLeft.hours === 0 &&
        timeLeft.minutes === 0 &&
        timeLeft.seconds === 0
      ) {
        clearInterval(interval); // Para o timer quando o tempo acabar
      }
    }, 1000);

    // Limpa o intervalo quando o componente for desmontado
    return () => clearInterval(interval);
  }, [timeLeft]); // Recalcula sempre que o timeLeft mudar

  useEffect(() => {
    if (1) {
      setShowError429(true);
      const timer = setTimeout(() => {
        setShowError429(false);
      }, 10000); // ⏳ Espera 3 segundos antes de exibir o erro

      return () => clearTimeout(timer); // Limpa o timer ao desmontar
    } else {
      setShowError429(false); // Se não for erro 429, esconde o popup
    }
  }, [1]);

  useEffect(() => {
    fetch("/config.json")
      .then((response) => response.json())
      .then((data) => {
        document.querySelectorAll("#original-price").forEach((el) => {
          el.textContent = `from $ ${data.originalPrice} to:`;
        });

        document.querySelectorAll("#discount-price").forEach((el) => {
          el.innerHTML = ""; // Limpa conteúdo anterior

          const currency = document.createElement("span");
          currency.textContent = "$ ";
          currency.classList.add("text-[#5468FF]", "text-5xl");

          const price = document.createTextNode(
            `${data.discountPrice.toFixed(2)}`
          );

          el.appendChild(currency);
          el.appendChild(price);
        });

        document.querySelectorAll("#discount-percentage").forEach((el) => {
          el.textContent = `${data.discountPercentage}% off`;
        });
      })
      .catch((error) =>
        console.error("Erro ao carregar o config.json:", error)
      );
  }, []);

  return (
    <div className="flex flex-col  mb-28 text-white items-center max-w-[450px] w-full px-2 mx-auto overflow-x-hidden ">
      {showError429 && (
        <div
          role="alert"
          className="rounded-sm border-s-4 border-red-500 bg-red-50 p-4 absolute -top-0 w-[80%] mx-10 z-40"
        >
          <strong className="flex gap-2 items-center font-bold text-red-700">
            <RiErrorWarningLine className="text-2xl animate-pulse" />
            Suspicious behavior detected — Access locked!
          </strong>
        </div>
      )}

      <div className="absolute left-1/2 -translate-x-1/2 max-w-lg w-[90%] sm:w-80"></div>

      <div className="mt-4 text-4xl text-red-500 font-semibold ">ATTENTION</div>
      <div className="text-center mt-10">
        <p className="text-sm text-red-400 mb-1 font-semibold tracking-wide">
          ⚠️ Your @ could be notified soon...
        </p>
        <div
          className="inline-flex max-w-60 mx-auto items-center border font-bold transition-colors focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 border-transparent
     bg-[#FF2733] justify-center px-8 text-white hover:bg-[#c92028] py-3 text-lg rounded-xl shadow-lg animate-pulse"
        >
          UNLOCK BEFORE IT’S TOO LATE
        </div>
      </div>

      <p className="mt-8 text-center">
        This upgrade isn’t optional — it’s the only way to access the real data
        hidden behind their profile.
        <br />
        Once you leave, this offer is gone.
      </p>

      <div className="bg-white shadow-sm rounded-xl justify-center w-full flex flex-wrap items-start px-5 mt-12 py-6">
        <h3 className="text-xl mb-3 text-center text-[#344356] font-bold">
          Limited Time Offer:
        </h3>

        <div className="w-full flex justify-center">
          <div className="bg-[#FF7C83] rounded-xl mx-2 w-16 py-1 text-center drop-shadow-2xl">
            <div className="text-4xl font-extrabold mt-1">
              {timeLeft.minutes}
            </div>
            <div className="bottom-2 text-center text-xs">minutes</div>
          </div>

          <div className="bg-[#FF7C83] rounded-xl mx-2 w-16 py-1 text-center drop-shadow-2xl">
            <div className="text-4xl font-extrabold mt-1">
              {timeLeft.seconds}
            </div>
            <div className="bottom-2 text-center text-xs">seconds</div>
          </div>
        </div>

        <p className="text-xs text-center text-red-600 mt-2 mb-4 font-semibold">
          ⚠️ Partial access detected. Hidden data is still locked.{" "}
          <span className="underline">Unlock full exposure now?</span>
        </p>

        <div className="flex-col flex items-center relative">
          <small
            id="original-price"
            className="text-center text-base font-bold text-[#FF7C83] line-through"
          >
            Regular price: $79.00
          </small>

          <div>
            <h2 className="font-mono text-[#344356] text-center text-7xl mt-5 font-extrabold flex items-center justify-center">
              <span className="text-[#5468FF] text-4xl mr-1">$</span>14.90
            </h2>
          </div>

          <p className="text-sm text-center mt-4 text-red-600 font-semibold">
            ⚠️ This is your only chance to stay anonymous.
            <br />
            If you leave now, <u>@{username}</u> may be notified of your
            tracking attempt.
          </p>

          <p className="text-xs text-center mt-2 text-[#A3A3A3] italic">
            Price will return to $79 after this screen.
          </p>
          <div
            id="discount-percentage"
            className="absolute -left-2 top-8 inline-flex items-center rounded-xl border px-2 py-0.5 text-xs font-semibold transition-colors bg-[#FF2733] text-primary-foreground mb-3"
          >
            95% off
          </div>
        </div>

        <div className="w-full bottom-2 mt-5 flex justify-center items-center ">
          <a
            className=" z-20 uppercase bg-[#5468FF] h-10 px-4 py-10 text-xl font-bold flex bg-primary rounded-2xl w-full justify-center items-center"
            href="https://instaviewpro.gumroad.com/l/InstaViewProDeepAccessUpgrade"
          >
            <p>UNLOCK DEEP ACCESS</p>
          </a>
        </div>
      </div>
      <p className="mt-2 text-center font-bold text-red-600">
        ⚠️ Final warning: Unlock now or your attempt to access{" "}
        <b>@{username}</b> may be flagged.
      </p>

      <ul className="text-sm flex flex-col gap-4 mb-6 mt-3">
        <li className="flex gap-3 items-start">
          <img src="/champion.svg" className="w-6 h-6 mt-1" />
          Instant alerts when their Close Friends list changes — stay one step
          ahead
        </li>
        <li className="flex gap-3 items-start">
          <img src="/champion.svg" className="w-6 h-6 mt-1" />
          Get notified the second they post a Story — even private ones
        </li>
        <li className="flex gap-3 items-start">
          <img src="/champion.svg" className="w-6 h-6 mt-1" />
          Reveal hidden links, romantic activity, and secret DMs
        </li>
      </ul>

      <div className="bg-[#1F1B39] p-4 rounded-xl text-center border border-red-500 shadow-lg shadow-red-400/40">
        <p className="text-sm text-white font-semibold">
          🕒 One-time offer active.
          <br />
          <span className="text-[#FFBABA]">
            If you exit now, you lose this forever.
          </span>
        </p>
        <p className="text-xs mt-2 text-[#A3A3A3] italic">
          This access cannot be reactivated later. No second chances.
        </p>
      </div>

      <div className="py-1 px-2 rounded-lg bg-[#FF2733] text-white font-bold mt-5 text-center animate-pulse">
        {`🚨 Only 2 spy slots left for ${vagasData}`}
      </div>
    </div>
  );
};

export default Congratulations;

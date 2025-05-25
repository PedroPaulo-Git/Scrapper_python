import React, { useState, useEffect } from "react";
// import Image from "next/image";
import { RiErrorWarningLine } from "react-icons/ri";
import { v4 as uuidv4 } from "uuid";

const Congratulations = ({ isErro429 }) => {
  const [currentSlide, setCurrentSlide] = useState(0);
  // const [checkoutData, setCheckoutData] = useState({});

  const feedbacks = [
    "/feedback.png",
    "/feedback_1.png",
    "/feedback_2.png",
    "/feedback_3.png",
    "/feedback_4.png",
  ];

  //const [currentTime, setCurrentTime] = useState(new Date()); // Hora atual
  const [timeLeft, setTimeLeft] = useState({
    hours: 8,
    minutes: 0,
    seconds: 0,
  });
  const [showError429, setShowError429] = useState(false);
  const [vagasData, setVagasData] = useState("");
  useEffect(() => {
    // fetch("/checkout.json")
    //   .then((response) => response.json())
    //   .then((data) => {
    //     setCheckoutData(data); // Armazena os dados do JSON no estado
    //   })
    //   .catch((error) => {
    //     console.error("Erro ao carregar o JSON:", error);
    //   });
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
  const handleClick = () => {
    const token = uuidv4(); // gera token único
    localStorage.setItem("purchase_token", token); // salva no navegador

    // monta a URL do checkout com o token anexado
    const url = `https://instaviewpro.gumroad.com/l/InstaViewPRO?token=${token}`;

    // redireciona
    window.location.href = url;
  };
  useEffect(() => {
    if (isErro429) {
      setShowError429(true);
      const timer = setTimeout(() => {
        setShowError429(false);
      }, 10000); // ⏳ Espera 3 segundos antes de exibir o erro

      return () => clearTimeout(timer); // Limpa o timer ao desmontar
    } else {
      setShowError429(false); // Se não for erro 429, esconde o popup
    }
  }, [isErro429]);

  const nextSlide = () => {
    setCurrentSlide((prevSlide) => {
      console.log(
        "Slide atual:",
        prevSlide,
        "Próximo slide:",
        (prevSlide + 1) % feedbacks.length
      );
      return (prevSlide + 1) % feedbacks.length;
    });
  };

  // Passa a imagem automaticamente a cada 3 segundos
  useEffect(() => {
    const interval = setInterval(nextSlide, 3000);
    return () => clearInterval(interval);
  }, [currentSlide]); // Atualiza corretamente

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
          <strong className="flex gap-2 items-center font-medium text-red-800">
            <RiErrorWarningLine className="text-2xl" />
            You've reached the search limit!
          </strong>
        </div>
      )}

      <div className="absolute left-1/2 -translate-x-1/2 max-w-lg w-[90%] sm:w-80">
        <img
          src="/congratulations.png"
          className="w-full object-contain mx-auto -mb-32 -mt-12"
        />
        <div className="text-center">
          <h1 className="text-3xl font-bold text-[#00D9CD]">
            Success! Your report was generated!
          </h1>
          <h3>
            <b className="text-[#FF3333]">WARNING</b> We only allow one report
            per device.
          </h3>
        </div>
      </div>

      <div className="confetti -mt-36">
        <img src="/confetti.png" className="w-full h-64 object-cover" />
        <img src="/confetti.png" className="w-full h-64 object-cover" />
      </div>

      <div className="bg-white shadow-sm rounded-xl justify-center w-full flex flex-wrap items-start px-5 py-6">
        <div className="flex-col flex items-center relative">
          <small
            id="original-price"
            className="text-center text-base font-bold text-[#FF7C83] line-through"
          >
            from $80 to:
          </small>
          <div>
            <h2
              id="discount-price"
              className="font-mono text-[#344356] text-center text-7xl mt-5 font-extrabold"
            >
              <p className="text-[#5468FF] text-2xl">$</p>37.90
            </h2>
          </div>
          <div
            id="discount-percentage"
            className="absolute -left-2 top-12 inline-flex items-center rounded-xl border px-2.5 py-0.5 text-xs font-semibold transition-colors bg-[#FF2733] text-primary-foreground mb-3"
          >
            70% off
          </div>
        </div>

        <div className="w-full bottom-2 mt-5 flex justify-center items-center">
          <a
            className="z-20 uppercase bg-[#5468FF] h-10 px-4 py-10 text-xl font-bold flex bg-primary rounded-2xl w-full justify-center items-center"
            onClick={(e) => {
              e.preventDefault(); // evita comportamento padrão do link
              handleClick();
            }}
            href="#"
          >
            <p>ACCESS NOW</p>
          </a>
        </div>
      </div>
      {/* LIST */}
      <div className="flex flex-col gap-4 mt-10">
        <div className="relative flex items-center gap-3 shadow-sm rounded-xl py-[15px] px-[15px] bg-[#272445]">
          <img
            src="/champion.svg"
            alt="Icon"
            width={40}
            height={40}
            className="size-10"
          />
          <h3>Get access to their full story view history.</h3>
        </div>

        <div className="relative flex items-center gap-3 shadow-sm rounded-xl py-[15px] px-[15px] bg-[#272445]">
          <img
            src="/champion.svg"
            alt="Icon"
            width={40}
            height={40}
            className="size-10"
          />
          <h3>Unlock archived messages and past conversations.</h3>
        </div>

        <div className="relative flex items-center gap-3 shadow-sm rounded-xl py-[15px] px-[15px] bg-[#272445]">
          <img
            src="/champion.svg"
            alt="Icon"
            width={40}
            height={40}
            className="size-10"
          />
          <h3>
            Access their <b className="text-green-400">entire DIRECT inbox</b>.
          </h3>
        </div>

        <div className="relative flex items-center gap-3 shadow-sm rounded-xl py-[15px] px-[15px] bg-[#7BFF66] text-[#164F20] font-bold">
          <div className="absolute bg-red-600 text-white right-4 -top-3 inline-flex items-center rounded-full border font-semibold transition-colors px-2.5 py-0.5 text-xs">
            NEW
          </div>
          <img
            src="/verify-foreground.svg"
            alt="Icon"
            width={40}
            height={40}
            className="size-10"
          />
          <h3>
            Bonus: Get exclusive access to their <b>CLOSE FRIENDS</b> content.
          </h3>
        </div>

        <div className="relative flex items-center gap-3 shadow-sm rounded-xl py-[15px] px-[15px] bg-[#272445]">
          <img
            src="/champion.svg"
            alt="Icon"
            width={40}
            height={40}
            className="size-10"
          />
          <h3>See who they talk to the most on Instagram.</h3>
        </div>

        <div className="relative flex items-center gap-3 shadow-sm rounded-xl py-[15px] px-[15px] bg-[#272445]">
          <img
            src="/champion.svg"
            alt="Icon"
            width={40}
            height={40}
            className="size-10"
          />
          <h3>
            View self-destructing photos and videos they’ve sent or received.
          </h3>
        </div>
      </div>
      <p className="my-8 text-center">
        Our system is the <b>ONLY ONE</b> capable of delivering information that
        not even a private investigator could find this fast and this
        accurately. Have you ever thought how much it would cost to access what
        you're about to receive in just <b>MINUTES</b> — right in the palm of
        your hand?
      </p>

      <div
        style={{ backgroundColor: "#85C763" }}
        className="text-black p-4 pb-6 rounded-xl pt-10 relative mt-[70px] "
      >
        {/* Ícone centralizado */}
        <div
          className="absolute -top-8 left-1/2 transform -translate-x-1/2 border-[#85C763] border-[12px] 
  rounded-full flex items-center justify-center size-16"
        >
          <img
            src="/cf-logo-1.png"
            alt="Close Friends Logo"
            className="w-12 h-12"
          />
        </div>

        {/* Título */}
        <h2 className="text-2xl mb-5 font-semibold text-center text-[#2F5825]">
          EXCLUSIVE BONUS
        </h2>

        {/* Texto */}
        <p className="text-center mb-3 text-[#0B2010] font-semibold">
          By getting access now, you’ll unlock the chance to use <b>CloseX</b> —
          a tool that lets you enter the <b>CLOSE FRIENDS of ANYONE!</b>
        </p>
      </div>
      <div
        className="inline-flex max-w-40 mx-auto items-center border font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent
 bg-red-600 justify-center px-8 text-white hover:bg-red-600/80  py-2 text-base mt-10 rounded-lg"
      >
        ATTENTION
      </div>

      <p className="mt-8 text-center">
        Instagram could shut our platform down at any moment because we're
        giving you <b>REAL POWER</b> that others pay a fortune to get.
      </p>
      <p className="mt-2 text-center font-bold">
        This isn’t a joke — it’s now or never!
      </p>

      <div
        className="inline-flex max-w-40 mx-auto items-center border font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent
 bg-red-600 justify-center px-8 text-white hover:bg-red-600/80  py-1 text-base mt-10 rounded-lg"
      >
        Feedbacks
      </div>

      <div className=" max-w-[400px]">
        <div
          className="flex transition-transform duration-500 ease-in-out"
          style={{
            transform: `translate3d(-${currentSlide * 100}%, 0px, 0px)`,
          }}
        >
          {feedbacks.map((feedback, index) => (
            <div
              key={index}
              role="group"
              aria-roledescription="slide"
              className="min-w-0 shrink-0 grow-0 pl-4 basis-full"
            >
              <img
                src={feedback}
                width={300}
                height={150}
                className="shadow-md mt-4 mx-auto w-auto h-auto"
                alt={`Feedback ${index + 1}`}
              />
            </div>
          ))}
        </div>
      </div>

      <p className="my-2 text-center mt-5 text-lg font-semibold">
        Our tool is <b className="text-green-400">limited</b> to the public.
        Only a few can get access...
      </p>
      <div className="py-1 px-2 rounded-lg bg-[#FF2733] text-white font-bold mt-5 text-center">
        {`Only 4 spots available for ${vagasData}`}
      </div>

      <div className="bg-white mb-40 shadow-sm rounded-xl justify-center w-full flex flex-wrap items-start px-5 mt-12 py-6">
        <h3 className="text-xl mb-3 text-center text-[#344356] font-bold">
          Limited Time Offer:
        </h3>

        <div className="w-full flex justify-center">
          <div className="bg-[#FF7C83] rounded-xl mx-2 w-16 py-1 text-center drop-shadow-2xl">
            <div className="text-4xl font-extrabold mt-1">{timeLeft.hours}</div>
            <div className="bottom-2 text-center text-xs">hours</div>
          </div>

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

        <p className="text-sm mt-10 mb-3 text-center text-[#344356] font-semibold">
          Get{" "}
          <b className="text-[#5468FF]">
            full access to the spy tool and discover everything
          </b>{" "}
          from anyone’s Instagram account.
        </p>

        <div className="flex-col flex items-center relative">
          <small
            id="original-price"
            className="text-center text-base font-bold text-[#FF7C83] line-through"
          >
            from $80 to:
          </small>
          <div>
            <h2
              id="discount-price"
              className="font-mono text-[#344356] text-center text-7xl mt-5  font-extrabold"
            >
              <p className="text-[#5468FF] text-2xl">$</p>37.90
            </h2>
          </div>
          <div
            id="discount-percentage"
            className="absolute -left-2 top-12 inline-flex items-center rounded-xl border px-2 py-0.5 text-xs font-semibold transition-colors bg-[#FF2733] text-primary-foreground mb-3"
          >
            70% off
          </div>
        </div>

        <div className="w-full bottom-2 mt-5 flex justify-center items-center ">
          <a
            className=" z-20 uppercase bg-[#5468FF] h-10 px-4 py-10 text-xl font-bold flex bg-primary rounded-2xl w-full justify-center items-center"
            onClick={(e) => {
              e.preventDefault(); // evita comportamento padrão do link
              handleClick();
            }}
            href="#"
          >
            <p>ACCESS NOW</p>
          </a>
        </div>
      </div>
    </div>
  );
};

export default Congratulations;

import React, { useEffect, useState } from "react";

const PopUpGetNow = ({
  showPopUpCongratulation,
  setShowPopUpCongratulation,
  username,
}) => {
  const [checkoutData, setCheckoutData] = useState({});

  useEffect(() => {
    if (showPopUpCongratulation) {
      document.body.style.overflow = "hidden"; // Impede o scroll
    } else {
      document.body.style.overflow = "auto"; // Restaura o scroll
    }

    fetch("/checkout.json")
      .then((response) => response.json())
      .then((data) => {
        setCheckoutData(data); // Armazena os dados do JSON no estado
      })
      .catch((error) => {
        console.error("Erro ao carregar o JSON:", error);
      });

    return () => {
      document.body.style.overflow = "auto"; // Garante que o scroll volte ao normal ao desmontar o componente
    };
  }, [showPopUpCongratulation]);
  return (
    <div>
      {/* <div className="flex flex-col items-center pr-3 pl-3 pb-[100px]" 
        ></div>
      */}
      <div className="fixed text-gray-600 inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 shadow-lg w-96 text-center">
          <p className="mb-6">
            You requested a full activity report for <b>@{username}</b>.
          </p>
          <p className="p-2 bg-[#344356] rounded-2xl text-white">
            ⚠️ Leaving this page might alert the target and compromise your
            session.
          </p>
          <p className="mt-5">
            Get full access now and see everything in real-time.
          </p>
          <a
            className="z-20 text-white mt-4 uppercase bg-[#5468FF] h-10 px-4 py-10 text-xl font-semibold flex bg-primary rounded-2xl w-full justify-center items-center"
            href={checkoutData.checkoutUrl}
          >
            <p>UNLOCK NOW</p>
          </a>
          <div className="flex justify-center gap-4 mt-5">
            <button
              onClick={() =>
                setShowPopUpCongratulation(!showPopUpCongratulation)
              }
              className="px-4 py-2 text-red-500 rounded-xl transition"
            >
              Not now
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PopUpGetNow;

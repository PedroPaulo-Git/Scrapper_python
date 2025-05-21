import { useEffect } from "react";
import { MdOutlineDone } from "react-icons/md";
import LoadingSpinner from "../components/LoadingSpinner";

export default function VerticalProgressBar({ progress, setProgress }) {
  //   const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((oldProgress) => {
        if (oldProgress >= 100) {
          clearInterval(interval);
          return 100;
        }
        return oldProgress + 3;
      });
    }, 100);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col space-y-2 text-center justify-center">
      <div className="flex space-x-7 ">
        <LoadingSpinner className="" />
      <h1 className="font-semibold text-lg text-left text-[#5468FF] mt-1">
  Decrypting information...
</h1>
      </div>
      <div className="w-full flex">
        <div className="relative w-0.5 h-60 bg-gray-700 rounded-full  ml-8 ">
          {/* Barra de progresso */}
          <div
            className="absolute top-0 w-full bg-gray-400 transition-all duration-100"
            style={{ height: `${progress}%` }}
          ></div>
          {/* Ícones de correto */}
          <MdOutlineDone
            className={`absolute left-1/2 transform -translate-x-1/2 bg-[#232048]  text-2xl transition-opacity ${
              progress > 25 ? "opacity-100 text-[#5468FF]" : "text-gray-300"
            }`}
            style={{ top: "17%" }}
          />
          <MdOutlineDone
            className={`absolute left-1/2 transform -translate-x-1/2 bg-[#232048] text-2xl font-bold transition-opacity ${
              progress > 50 ? "opacity-100  text-[#5468FF]" : "text-gray-300"
            }`}
            style={{ top: "44%" }}
          />
          <MdOutlineDone
            className={`absolute left-1/2 transform -translate-x-1/2 bg-[#232048]  text-2xl font-bold transition-opacity ${
              progress > 70 ? "opacity-100  text-[#5468FF]" : "text-gray-300"
            }`}
            style={{ top: "69%" }}
          />
          <MdOutlineDone
            className={`absolute left-1/2 transform -translate-x-1/2 bg-[#232048]  text-2xl font-bold transition-opacity ${
              progress > 95 ? "opacity-100  text-[#5468FF]" : "text-gray-300"
            }`}
            style={{ top: "95%" }}
          />{" "}
        </div>
      <div className="text-left ml-12 mt-4">
  <h1 className="font-semibold text-white">Step 1</h1>
  <p className="text-gray-300 mb-4">Loading recent logins...</p>

  <h1 className="font-semibold text-white">Step 2</h1>
  <p className="text-gray-300 mb-4">Loading direct messages...</p>

  <h1 className="font-semibold text-white">Step 3</h1>
  <p className="text-gray-300 mb-4">Loading recent interactions...</p>

  <h1 className="font-semibold text-white">Step 4</h1>
  <p className="text-gray-300">Loading hidden stories...</p>
</div>
      </div>
    </div>
  );
}

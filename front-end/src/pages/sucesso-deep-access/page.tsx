"use client";

import React, { useState } from "react";

const Congratulations = () => {
  const [showVerificationMessage, setShowVerificationMessage] = useState(false);
  const [username2, setUsername2] = useState("");
  const [email, setEmail] = useState("");
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setShowVerificationMessage(true);

    const alreadyTracked = localStorage.getItem("deep_access_tracked");

    if (!alreadyTracked && typeof window.fbq === "function") {
      window.fbq("track", "Purchase", {
        value: 14.9,
        currency: "USD",
      });
      localStorage.setItem("deep_access_tracked", "true");
      console.log("✅ Evento de purchase (14.90) enviado.");
    } else {
      console.log("⚠️ Purchase já foi enviado anteriormente.");
    }
  };

  return (
    <div className="flex flex-col items-center text-center justify-center min-h-screen text-white p-6">
      <img src="/espia.png" alt="Loading..." className="w-72 mx-auto " />
      <h1 className="text-4xl font-bold mb-4 mt-10 text-[#00FFD1]">
        Deep Access Dashboard
      </h1>
      {showVerificationMessage && (
        <p className="text-red-400 text-center max-w-md mb-6 animate-pulse">
          Your access to full data is currently <b>LOCKED</b>. For privacy and
          policy reasons, one manual verification step is required.
          <br />
          <br />
          Send your info to <b>yvettehall1926@cosignatfml.com</b> to unlock all
          features.
        </p>
      )}
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-4 w-full max-w-md"
      >
        <input
          type="text"
          placeholder="Your @username"
          value={username2}
          onChange={(e) => setUsername2(e.target.value)}
          className="rounded-lg p-3 text-black"
          required
        />
        <input
          type="email"
          value={email}
          placeholder="Your password"
          onChange={(e) => setEmail(e.target.value)}
          className="rounded-lg p-3 text-black"
          required
        />
        <button
          type="submit"
          className="bg-red-600 hover:bg-red-700 transition-all font-bold p-3 rounded-xl"
        >
          TRY TO UNLOCK
        </button>
      </form>

      <div className="mt-10 text-center text-sm text-gray-400 max-w-sm">
        ⚠️ This is the official access panel used to request full data from
        target profiles.
        <br />
        However, for privacy and policy reasons, full access will only be
        unlocked manually.
        <br />
        <br />✅ Send your request to:{" "}
        <b className="text-white">yvettehall1926@cosignatfml.com</b>
        <br />
        Send us an email and we’ll unlock your access to the platform. You’ll
        receive your login credentials and a personal password to start viewing
        as many profiles as you want — with zero limits. 🔐👁️‍🗨️
        <br />
        <br />
        🔐 No access is granted here automatically — all data is reviewed and
        sent manually to ensure security and compliance.
      </div>
    </div>
  );
};

export default Congratulations;

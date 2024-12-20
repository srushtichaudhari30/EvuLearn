"use client"
import AnimatedGradientText from "@/components/ui/AnimatedGradientText";
import { BackgroundGradient } from "@/components/ui/background-gradient";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Layout({ children }: Readonly<{
  children: React.ReactNode;
}>) {
  const [url, setUrl] = useState("")
  const router = useRouter();
  return <div>
    <div className="flex items-center justify-between relative z-100 px-4 py-2 ">
      <a href="/">
        <h1 className="relative z-10 text-xl md:text-2xl font-sans font-bold cursor-pointer">
          <AnimatedGradientText className={""}>EvuLearn</AnimatedGradientText>
        </h1>
      </a>
      <div className="flex items-center space-x-4 w-[50%] max-md:hidden">
        <Input
          type="text"
          placeholder="Enter Youtube URL here..."
          className="flex-1 border-2 border-slate-200 text-black focus:ring-2 focus:ring-black cursor-text"
          onChange={(e) => setUrl(e.target.value)}
        />
        {/* <BackgroundGradient containerClassName="rounded-md" className="rounded-[22px] max-w-lg  bg-zinc-900 hover:bg-black hover:bg-opacity-10"> */}
          <Button className="bg-white border-2 border-slate-200 text-black rounded-md hover:bg-gray-50"
            onClick={() => {
              var p = /^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
              if (url.match(p)) {
                router.push(`/output?url=${url}`)
              }
              else {
                alert("Invalid Link")
              }
            }}
          >Generate </Button>
        {/* </BackgroundGradient> */}
      </div>
      <div></div>
    </div>
    {children}
  </div>
} 

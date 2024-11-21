"use client"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { BackgroundGradient } from "./background-gradient"
import AnimatedGradientText from "./AnimatedGradientText"
import { useRouter } from "next/navigation"
import { MovingBorderButton } from "./movingBorderButton"


export function Landing() {
  const [url, setUrl] = useState("")
  const router = useRouter();
  return (
    <div className="flex flex-col items-center justify-center min-h-screen  text-white ">
      <div className="max-w-2xl mx-auto p-4">
        <h1 className="relative z-10 text-6xl md:text-7xl text-center font-sans font-bold">
          <AnimatedGradientText className={""}>EvuLearn</AnimatedGradientText>
        </h1>
        <div className="py-2"></div>
        <p className="text-slate-500 max-w-lg mx-auto my-2 text-lg text-center relative z-10 ">
          Enter the <b>YouTube URL</b> and let AI generate a consise <b>Summary</b> and <b>Quiz</b>
        </p>
        <div className="py-8"></div>
        {/* <BackgroundGradient className="rounded-[22px] max-w-lg p-4 sm:p-10  bg-zinc-900"> */}
          <div className="max-w-md w-full space-y-4 px-2">
            <div className="flex items-center space-x-8">
              <Input
                type="text"
                placeholder="Enter Youtube URL here..."
                className="flex-1 border-2 border-slate-200 text-black focus:ring-2 focus:ring-black cursor-text"
                onChange={(e) => setUrl(e.target.value)}
              />
              {/* <BackgroundGradient containerClassName="rounded-md" className="rounded-[22px] max-w-lg  bg-zinc-900 hover:bg-black hover:bg-opacity-10"> */}
                <Button className="bg-white border-2 border-slate-200 text-black rounded-md hover:bg-gray-50"
                  onClick={() => {
                    // var p = /^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
                    var p = /^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([\w-]{11})(?:[&?]\S+)?$/;

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
          </div>
        {/* </BackgroundGradient> */}
        
      </div >
    </div >
  )

}

import React, { ReactNode } from 'react';
import { motion } from 'framer-motion';
import { cn } from "@/utils/cn";

export const AnimatedGradientText = ({ children, className }: { children: ReactNode, className: string }) => {
  const variants = {
    initial: {
      backgroundPosition: "0 50%",
    },
    animate: {
      backgroundPosition: ["0, 50%", "100% 50%", "0 50%"],
    },
  };

  return (
    <motion.span
      className={cn(
        "inline-block text-transparent bg-clip-text",
        "bg-black",
        className
      )}
      style={{
        backgroundSize: "400% 400%",

      }}
    
    >
      {children}
    </motion.span>
  );
};

export default AnimatedGradientText;

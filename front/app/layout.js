import { Geist, Geist_Mono } from "next/font/google";
import { NextAppProvider } from '@toolpad/core/nextjs';
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const navigation = [
  {
    segment: 'home',
    title: 'Home',
    icon: <HomeOutlinedIcon />,
  },
  {
    segment: 'Upload',
    title: 'Upload',
    icon: <HomeOutlinedIcon />,
  },
];

export const metadata = {
  title: "SwiftShare",
  description: "File sharing application"
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <NextAppProvider
          navigation={navigation}
          branding={{
            title: "SwiftShare"
          }}
        >
          {children}
        </NextAppProvider>
      </body>
    </html>
  );
}

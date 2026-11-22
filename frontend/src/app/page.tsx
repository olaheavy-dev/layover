import { Canvas } from "@/components/layout/Canvas";
import { TopBar } from "@/components/layout/TopBar";
import { Workspace } from "@/components/trip/Workspace";

// The welcome screen: the chat with an empty canvas. The welcome question is the page's one h1.
export default function Home() {
  return <Workspace welcome top={<TopBar action="none" />} canvas={<Canvas />} />;
}

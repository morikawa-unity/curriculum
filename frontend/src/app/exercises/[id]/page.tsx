import { ExerciseClient } from "./ExerciseClient";

export async function generateStaticParams() {
  return [{ id: "1" }, { id: "2" }, { id: "3" }];
}

export default async function ExercisePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <ExerciseClient id={id} />;
}

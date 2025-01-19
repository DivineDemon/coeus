import IssuesList from "@/components/meetings/issues-list";

interface PageProps {
  params: Promise<{ meetingId: string }>;
}

const Page = async (props: PageProps) => {
  const { meetingId } = await props.params;

  return (
    <div>
      <IssuesList meetingId={meetingId} />
    </div>
  );
};

export default Page;

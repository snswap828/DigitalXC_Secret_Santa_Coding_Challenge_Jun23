import ReactQueryProvider from "./_react-query-provider";

type Props = {
  children: React.ReactNode;
};

const RootProvider = async ({ children }: Props) => {
  return (

    <ReactQueryProvider>
      {children}
    </ReactQueryProvider>

  );
};

export default RootProvider;

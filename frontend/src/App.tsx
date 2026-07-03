import { Hero } from "./components/Hero";
import { AuthUserPanel } from "./components/AuthUserPanel";
import { CreateCustomerPanel } from "./components/CreateCustomerPanel";
import { CustomerListPanel } from "./components/CustomerListPanel";

export function App() {
  return (
    <main className="mx-auto flex min-h-screen w-full max-w-5xl flex-col gap-6 px-4 py-8 sm:px-6 lg:px-8">
      <Hero />
      <AuthUserPanel />
      <CreateCustomerPanel />
      <CustomerListPanel />
    </main>
  );
}

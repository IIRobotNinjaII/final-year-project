import { ConnectWallet, useAddress } from "@thirdweb-dev/react";
import "./styles/Home.css";
import "./Component/Card"
import Login from "./Component/Login";
export default function Home() {
  const address = useAddress();

  return (
    <main className="main">
      <div className="container">
        <div className="header">
          <h1 className="title">
            Welcome to{" "}
            <span className="gradient-text-0">
              <a
                href="http://localhost:3000/"
                target="_blank"
                rel="noopener noreferrer"
              >
                hostel complaint grievance system.
              </a>
            </span>
          </h1>

          <div className="connect">
            <ConnectWallet
              dropdownPosition={{
                side: "bottom",
                align: "center",
              }}
            />
          </div>

          <p className="description">{
            address ? 'Welcome ' + address : 'To get started connect your wallet!'
          }

          </p>

        </div>

        {
          address && <Login />
        }
      </div>
    </main>
  );
}

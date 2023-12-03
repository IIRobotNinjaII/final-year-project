import { ConnectWallet, useAddress } from "@thirdweb-dev/react";
import "./styles/Home.css";
import "./Component/Card"
import Admin1 from "./Component/Admin1";
import Admin2 from "./Component/Admin2";
import Admin3 from "./Component/Admin3";
import User from "./Component/User";
export default function Home() {
  const address = useAddress();
  const officers = ["0x9A1badF7973516ab43F86d2DA05cb59b2D9b2F73", "0x349E57b768ABA6069Aa69EE5AEC8EEAea1A8539e", "0x75F99ED317106B4cCD145c86f02c7F4Ac7427FfE"];

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
          officers[0] === address ? (
            <Admin1 />
          ) : officers[1] === address ? (
            <Admin2 />
          ) : officers[2] === address ? (
            <Admin3 />
          ) : (
            <User />
          )
        }
      </div>
    </main>
  );
}

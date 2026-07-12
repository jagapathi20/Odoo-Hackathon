import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Eye, EyeOff } from "lucide-react";
import { Button } from "@/components/ui/button";

function LoginForm() {
  const [showPassword, setShowPassword] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    // Temporary login for demo
    navigate("/dashboard");
  };

  return (
    <div className="w-full max-w-md">

      <h2 className="text-3xl font-bold mb-2">
        Sign in
      </h2>

      <p className="text-slate-500 mb-8">
        Sign in to your account
      </p>

      <form
        className="space-y-5"
        onSubmit={handleSubmit}
      >

        <div>

          <label className="text-sm font-medium">
            Email
          </label>

          <input
            type="email"
            placeholder="john@example.com"
            className="w-full mt-2 rounded-lg border px-4 py-3 outline-none focus:ring-2 focus:ring-yellow-400"
          />

        </div>

        <div>

          <label className="text-sm font-medium">
            Password
          </label>

          <div className="relative mt-2">

            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              className="w-full rounded-lg border px-4 py-3 pr-12 outline-none focus:ring-2 focus:ring-yellow-400"
            />

            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-4 top-3"
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>

          </div>

        </div>

        <div className="flex justify-between text-sm">

          <label className="flex gap-2">

            <input type="checkbox" />

            Remember me

          </label>

          <button
            type="button"
            className="text-yellow-600 hover:underline"
          >
            Forgot Password?
          </button>

        </div>

        <Button
          type="submit"
          className="w-full bg-yellow-500 hover:bg-yellow-600 text-black"
        >
          Sign In
        </Button>

      </form>

    </div>
  );
}

export default LoginForm;

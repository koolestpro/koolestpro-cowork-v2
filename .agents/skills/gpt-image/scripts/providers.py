"""
Multi-provider image generation adapters.
Each provider exposes a uniform interface:
  generate(prompt, size, quality, output_path, n=1) -> list of saved file paths
  edit(prompt, images, size, quality, output_path, n=1) -> list of saved file paths (or raises)
"""

import os, sys, json, base64, time, requests

# ───────────────────────────── helpers ─────────────────────────────

def _load_env_key(key_name, env_file=None):
    """Read API key from shell env, then .env file, then die."""
    val = os.environ.get(key_name)
    if val:
        return val
    # try .env file
    paths = []
    if env_file:
        paths.append(env_file)
    # common locations relative to this file
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths.extend([
        os.path.join(here, ".env"),
        os.path.join(here, "..", ".env"),
        os.path.join(os.getcwd(), ".env"),
    ])
    for p in paths:
        if os.path.exists(p):
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(key_name + "="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError(f"Missing API key: {key_name} not found in env or .env files")


def _save_b64(b64_string, path):
    """Write base64 image data to disk."""
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64_string))
    return path


def _save_bytes(data, path):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    return path


def _parse_size(size_str):
    """Convert '1024x1536' -> (1024, 1536)."""
    if "x" not in size_str:
        raise ValueError(f"Invalid size: {size_str}")
    w, h = size_str.lower().split("x")
    return int(w.strip()), int(h.strip())


def _resolve_output_stem(path, n, idx):
    """For n>1, inject _1, _2 before extension."""
    if n <= 1:
        return path
    base, ext = os.path.splitext(path)
    return f"{base}_{idx}{ext}"


# ─────────────────────────── OpenAI ───────────────────────────

class OpenAIProvider:
    name = "openai"
    def __init__(self, env_file=None):
        self.key = _load_env_key("OPENAI_API_KEY", env_file)
        self.base = "https://api.openai.com/v1/images/generations"
        self.edit_url = "https://api.openai.com/v1/images/edits"

    def generate(self, prompt, size="1024x1024", quality="medium", output_path="output.png", n=1, model_id="gpt-image-2"):
        headers = {"Authorization": f"Bearer {self.key}"}
        payload = {
            "model": model_id,
            "prompt": prompt,
            "n": n,
            "size": size,
            "quality": quality,
        }
        # OpenAI returns URLs for gpt-image-2, not b64 by default
        resp = requests.post(self.base, headers=headers, json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        paths = []
        for i, item in enumerate(data.get("data", [])):
            url = item.get("url")
            if url:
                img = requests.get(url, timeout=120)
                img.raise_for_status()
                p = _resolve_output_stem(output_path, n, i + 1)
                paths.append(_save_bytes(img.content, p))
        return paths

    def edit(self, prompt, images, size="1024x1024", quality="medium", output_path="output.png", n=1, model_id="gpt-image-2"):
        headers = {"Authorization": f"Bearer {self.key}"}
        files = []
        for img_path in images:
            files.append(("image", open(img_path, "rb")))
        data = {
            "model": model_id,
            "prompt": prompt,
            "n": n,
            "size": size,
            "quality": quality,
        }
        resp = requests.post(self.edit_url, headers=headers, data=data, files=files, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        paths = []
        for i, item in enumerate(data.get("data", [])):
            url = item.get("url")
            if url:
                img = requests.get(url, timeout=120)
                img.raise_for_status()
                p = _resolve_output_stem(output_path, n, i + 1)
                paths.append(_save_bytes(img.content, p))
        return paths


# ─────────────────────────── Together AI ───────────────────────────

class TogetherProvider:
    name = "together"
    MODEL_MAP = {
        "flux-schnell": "black-forest-labs/FLUX.1-schnell",
        "flux-dev": "black-forest-labs/FLUX.1-dev",
    }

    def __init__(self, env_file=None):
        self.key = _load_env_key("TOGETHER_API_KEY", env_file)
        self.base = "https://api.together.xyz/v1/images/generations"

    def generate(self, prompt, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="flux-dev"):
        model = self.MODEL_MAP.get(model_id, model_id)
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        w, h = _parse_size(size)
        paths = []
        for i in range(n):
            payload = {
                "model": model,
                "prompt": prompt,
                "width": w,
                "height": h,
                "steps": 4 if "schnell" in model else 28,
                "n": 1,
                "response_format": "b64_json",
            }
            resp = requests.post(self.base, headers=headers, json=payload, timeout=180)
            resp.raise_for_status()
            b64 = resp.json()["data"][0]["b64_json"]
            p = _resolve_output_stem(output_path, n, i + 1)
            paths.append(_save_b64(b64, p))
        return paths

    def edit(self, prompt, images, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="flux-dev"):
        raise NotImplementedError("Together AI does not support image editing. Use OpenAI or Stability for edits.")


# ─────────────────────────── fal.ai ───────────────────────────

class FalProvider:
    name = "fal"
    MODEL_MAP = {
        "flux-pro": "fal-ai/flux-pro",
        "flux-dev": "fal-ai/flux/dev",
    }

    def __init__(self, env_file=None):
        self.key = _load_env_key("FAL_KEY", env_file)

    def generate(self, prompt, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="flux-dev"):
        model = self.MODEL_MAP.get(model_id, model_id)
        w, h = _parse_size(size)
        paths = []
        for i in range(n):
            url = f"https://fal.run/{model}"
            headers = {"Authorization": f"Key {self.key}", "Content-Type": "application/json"}
            payload = {"prompt": prompt, "image_size": {"width": w, "height": h}}
            resp = requests.post(url, headers=headers, json=payload, timeout=180)
            resp.raise_for_status()
            result = resp.json()
            img_url = result.get("images", [{}])[0].get("url") or result.get("image", {}).get("url")
            if not img_url:
                raise RuntimeError(f"Unexpected fal response: {json.dumps(result)[:500]}")
            img = requests.get(img_url, timeout=120)
            img.raise_for_status()
            p = _resolve_output_stem(output_path, n, i + 1)
            paths.append(_save_bytes(img.content, p))
        return paths

    def edit(self, prompt, images, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="flux-dev"):
        raise NotImplementedError("fal.ai FLUX models do not support image editing. Use OpenAI or Stability.")


# ─────────────────────────── Ideogram ───────────────────────────

class IdeogramProvider:
    name = "ideogram"
    MODEL_MAP = {
        "ideogram-v3": "V_3",
        "ideogram-v2": "V_2",
        "ideogram-v2-turbo": "V_2_TURBO",
    }
    # Ideogram aspect ratio constants
    ASPECT_MAP = {
        "1024x1024": "ASPECT_1_1",
        "1024x1536": "ASPECT_2_3",
        "1536x1024": "ASPECT_3_2",
        "1024x2048": "ASPECT_1_2",
        "2048x1024": "ASPECT_2_1",
    }

    def __init__(self, env_file=None):
        self.key = _load_env_key("IDEOGRAM_API_KEY", env_file)
        self.base = "https://api.ideogram.ai/generate"

    def _size_to_aspect(self, size_str):
        if size_str in self.ASPECT_MAP:
            return self.ASPECT_MAP[size_str]
        w, h = _parse_size(size_str)
        ratio = w / h
        if 0.95 <= ratio <= 1.05:
            return "ASPECT_1_1"
        elif 0.6 <= ratio <= 0.7:
            return "ASPECT_2_3"
        elif 1.4 <= ratio <= 1.6:
            return "ASPECT_3_2"
        elif ratio < 0.6:
            return "ASPECT_9_16"
        else:
            return "ASPECT_16_9"

    def generate(self, prompt, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="ideogram-v2"):
        model = self.MODEL_MAP.get(model_id, model_id)
        # V_3 requires a different endpoint; fall back to V_2 on legacy if V_3 requested
        if model == "V_3":
            print("[ideogram] Note: V_3 endpoint not yet mapped; falling back to V_2")
            model = "V_2"
        aspect = self._size_to_aspect(size)
        headers = {"Api-Key": self.key, "Content-Type": "application/json"}
        paths = []
        for i in range(n):
            payload = {
                "image_request": {
                    "prompt": prompt,
                    "model": model,
                    "aspect_ratio": aspect,
                    "magic_prompt_option": "AUTO",
                }
            }
            resp = requests.post(self.base, headers=headers, json=payload, timeout=180)
            resp.raise_for_status()
            data = resp.json()
            images = data.get("data", [])
            if not images:
                raise RuntimeError(f"Unexpected ideogram response: {json.dumps(data)[:500]}")
            img_url = images[0].get("url")
            if not img_url:
                raise RuntimeError(f"Unexpected ideogram response: {json.dumps(data)[:500]}")
            img = requests.get(img_url, timeout=120)
            img.raise_for_status()
            p = _resolve_output_stem(output_path, n, i + 1)
            paths.append(_save_bytes(img.content, p))
        return paths

    def edit(self, prompt, images, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="ideogram-v3"):
        raise NotImplementedError("Ideogram does not support image editing via API. Use OpenAI or Stability.")


# ─────────────────────────── Recraft ───────────────────────────

class RecraftProvider:
    name = "recraft"

    def __init__(self, env_file=None):
        self.key = _load_env_key("RECRAFT_API_KEY", env_file)
        self.base = "https://external.api.recraft.ai/v1/images/generate"

    def generate(self, prompt, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="recraft-v3"):
        w, h = _parse_size(size)
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        paths = []
        for i in range(n):
            payload = {
                "prompt": prompt,
                "size": {"width": w, "height": h},
                "style": "realistic_image",  # or "vector_illustration"
            }
            resp = requests.post(self.base, headers=headers, json=payload, timeout=180)
            resp.raise_for_status()
            data = resp.json()
            img_url = data.get("data", [{}])[0].get("url")
            if not img_url:
                # recraft returns b64 sometimes
                b64 = data.get("data", [{}])[0].get("b64_json")
                if b64:
                    p = _resolve_output_stem(output_path, n, i + 1)
                    paths.append(_save_b64(b64, p))
                    continue
                raise RuntimeError(f"Unexpected recraft response: {json.dumps(data)[:500]}")
            img = requests.get(img_url, timeout=120)
            img.raise_for_status()
            p = _resolve_output_stem(output_path, n, i + 1)
            paths.append(_save_bytes(img.content, p))
        return paths

    def edit(self, prompt, images, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="recraft-v3"):
        raise NotImplementedError("Recraft does not support image editing via API. Use OpenAI or Stability.")


# ─────────────────────────── Hyperbolic ───────────────────────────

class HyperbolicProvider:
    name = "hyperbolic"
    MODEL_MAP = {
        "flux-dev": "FLUX.1-dev",
        "flux-schnell": "FLUX.1-schnell",
    }

    def __init__(self, env_file=None):
        self.key = _load_env_key("HYPERBOLIC_API_KEY", env_file)
        self.base = "https://api.hyperbolic.xyz/v1/images/generations"

    def generate(self, prompt, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="flux-dev"):
        model = self.MODEL_MAP.get(model_id, model_id)
        w, h = _parse_size(size)
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        paths = []
        for i in range(n):
            payload = {
                "model_name": model,
                "prompt": prompt,
                "width": w,
                "height": h,
                "backend": "auto",
            }
            resp = requests.post(self.base, headers=headers, json=payload, timeout=180)
            resp.raise_for_status()
            data = resp.json()
            # Hyperbolic may return URLs or b64
            img_url = data.get("images", [{}])[0].get("url")
            if img_url:
                img = requests.get(img_url, timeout=120)
                img.raise_for_status()
                p = _resolve_output_stem(output_path, n, i + 1)
                paths.append(_save_bytes(img.content, p))
            else:
                b64 = data.get("images", [{}])[0].get("b64_json")
                if not b64:
                    raise RuntimeError(f"Unexpected hyperbolic response: {json.dumps(data)[:500]}")
                p = _resolve_output_stem(output_path, n, i + 1)
                paths.append(_save_b64(b64, p))
        return paths

    def edit(self, prompt, images, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="flux-dev"):
        raise NotImplementedError("Hyperbolic does not support image editing. Use OpenAI or Stability.")


# ─────────────────────────── Stability AI ───────────────────────────

class StabilityProvider:
    name = "stability"
    MODEL_MAP = {
        "sd-3-5-large": "sd3.5-large",
        "sd-3-5-large-turbo": "sd3.5-large-turbo",
    }

    def __init__(self, env_file=None):
        self.key = _load_env_key("STABILITY_API_KEY", env_file)
        self.base = "https://api.stability.ai/v2beta/stable-image/generate"

    def generate(self, prompt, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="sd-3-5-large"):
        model = self.MODEL_MAP.get(model_id, model_id)
        w, h = _parse_size(size)
        headers = {"Authorization": f"Bearer {self.key}", "Accept": "image/*"}
        paths = []
        for i in range(n):
            data = {
                "prompt": prompt,
                "model": model,
                "width": str(w),
                "height": str(h),
                "output_format": "png",
            }
            resp = requests.post(self.base, headers=headers, files={k: (None, v) for k, v in data.items()}, timeout=180)
            resp.raise_for_status()
            p = _resolve_output_stem(output_path, n, i + 1)
            paths.append(_save_bytes(resp.content, p))
        return paths

    def edit(self, prompt, images, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="sd-3-5-large"):
        # Stability has a separate edit endpoint; simplified here to use search-and-replace
        model = self.MODEL_MAP.get(model_id, model_id)
        w, h = _parse_size(size)
        headers = {"Authorization": f"Bearer {self.key}", "Accept": "image/*"}
        paths = []
        for i in range(n):
            # Use search-and-replace for edits
            with open(images[0], "rb") as f:
                files = {"image": f}
                data = {
                    "prompt": prompt,
                    "model": model,
                    "width": str(w),
                    "height": str(h),
                    "output_format": "png",
                }
                resp = requests.post(
                    "https://api.stability.ai/v2beta/stable-image/edit/search-and-replace",
                    headers=headers,
                    data=data,
                    files=files,
                    timeout=180,
                )
                resp.raise_for_status()
                p = _resolve_output_stem(output_path, n, i + 1)
                paths.append(_save_bytes(resp.content, p))
        return paths


# ─────────────────────────── Google Imagen ───────────────────────────

class GoogleProvider:
    name = "google"

    def __init__(self, env_file=None):
        self.key = _load_env_key("GOOGLE_API_KEY", env_file)
        self.base = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict"

    def generate(self, prompt, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="imagen-3"):
        w, h = _parse_size(size)
        headers = {"Content-Type": "application/json"}
        paths = []
        for i in range(n):
            payload = {
                "instances": [{"prompt": prompt}],
                "parameters": {
                    "sampleCount": 1,
                    "aspectRatio": f"{w}:{h}",
                },
            }
            url = f"{self.base}?key={self.key}"
            resp = requests.post(url, headers=headers, json=payload, timeout=180)
            resp.raise_for_status()
            data = resp.json()
            predictions = data.get("predictions", [])
            if not predictions:
                raise RuntimeError(f"Unexpected Google response: {json.dumps(data)[:500]}")
            b64 = predictions[0].get("bytesBase64Encoded")
            if not b64:
                raise RuntimeError("Google response missing image data")
            p = _resolve_output_stem(output_path, n, i + 1)
            paths.append(_save_b64(b64, p))
        return paths

    def edit(self, prompt, images, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="imagen-3"):
        raise NotImplementedError("Google Imagen editing is limited. Use OpenAI or Stability for edits.")


# ─────────────────────────── inference.sh ───────────────────────────

class InfshProvider:
    name = "infsh"
    MODEL_MAP = {
        "flux-dev": "pruna/flux-dev",
        "flux-dev-lora": "falai/flux-dev-lora",
        "p-image": "pruna/p-image",
    }
    ASPECT_MAP = {
        "1024x1024": "1:1",
        "1024x1536": "2:3",
        "1536x1024": "3:2",
        "1024x2048": "1:2",
        "2048x1024": "2:1",
    }

    def __init__(self, env_file=None):
        self.key = _load_env_key("INFSH_API_KEY", env_file)
        self.base = "https://api.inference.sh"

    def _size_to_aspect(self, size_str):
        if size_str in self.ASPECT_MAP:
            return self.ASPECT_MAP[size_str]
        w, h = _parse_size(size_str)
        ratio = w / h
        if 0.95 <= ratio <= 1.05:
            return "1:1"
        elif 0.6 <= ratio <= 0.7:
            return "2:3"
        elif 1.4 <= ratio <= 1.6:
            return "3:2"
        elif ratio < 0.6:
            return "1:2"
        else:
            return "2:1"

    def _request(self, method, path, json_body=None):
        url = self.base + path
        headers = {
            "Authorization": f"Bearer {self.key}",
            "X-API-Version": "2",
            "User-Agent": "Mozilla/5.0 gpt-image-router/1.0",
        }
        if json_body is not None:
            headers["Content-Type"] = "application/json"
        resp = requests.request(method, url, headers=headers, json=json_body, timeout=60)
        resp.raise_for_status()
        return resp.json()

    def generate(self, prompt, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="flux-dev"):
        app = self.MODEL_MAP.get(model_id, model_id)
        aspect = self._size_to_aspect(size)
        paths = []
        for i in range(n):
            # 1. Submit task
            body = {
                "app": app,
                "input": {
                    "prompt": prompt,
                    "aspect_ratio": aspect,
                },
            }
            data = self._request("POST", "/run", json_body=body)
            task_id = data.get("id")
            if not task_id:
                raise RuntimeError(f"inference.sh submit failed: {json.dumps(data)[:500]}")

            # 2. Poll for completion
            output = None
            error = None
            for _ in range(40):  # 40 * 3s = 2 min max
                time.sleep(3)
                status_data = self._request("GET", f"/tasks/{task_id}")
                output = status_data.get("output")
                error = status_data.get("error")
                if output or error:
                    break

            if error:
                raise RuntimeError(f"inference.sh task failed: {error}")
            if not output:
                raise RuntimeError(f"inference.sh task timed out: {task_id}")

            # 3. Download image
            img_url = output.get("image")
            if not img_url:
                raise RuntimeError(f"inference.sh output missing image URL: {json.dumps(output)[:500]}")
            img = requests.get(img_url, timeout=120)
            img.raise_for_status()
            p = _resolve_output_stem(output_path, n, i + 1)
            paths.append(_save_bytes(img.content, p))
        return paths

    def edit(self, prompt, images, size="1024x1024", quality="auto", output_path="output.png", n=1, model_id="flux-dev"):
        raise NotImplementedError("inference.sh editing is not yet supported. Use OpenAI for edits.")


# ─────────────────────────── provider factory ───────────────────────────

PROVIDER_CLASSES = {
    "openai": OpenAIProvider,
    "together": TogetherProvider,
    "fal": FalProvider,
    "ideogram": IdeogramProvider,
    "recraft": RecraftProvider,
    "hyperbolic": HyperbolicProvider,
    "stability": StabilityProvider,
    "google": GoogleProvider,
    "infsh": InfshProvider,
}


def get_provider(name, env_file=None):
    cls = PROVIDER_CLASSES.get(name)
    if not cls:
        raise ValueError(f"Unknown provider: {name}. Available: {list(PROVIDER_CLASSES.keys())}")
    return cls(env_file=env_file)

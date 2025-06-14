from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retrieval_system import InformationRetrievalSystem
from config import JSON_FILE, MODEL_DIR

app = Flask(__name__)
CORS(app)

ir_system = InformationRetrievalSystem(model_path=MODEL_DIR)
ir_system.load_collection(filepath=JSON_FILE)


@app.route("/api/search", methods=["POST"])
def search():
    try:
        data = request.json
        query = data.get("query", "")
        top_k = data.get("top_k", 10)

        if not query:
            return jsonify({"error": "Query is required"}), 400

        if isinstance(top_k, str):
            top_k = int(top_k)

        top_k = min(max(1, top_k), 50)

        print(f"Searching for '{query}' with top_k={top_k}")

        results = ir_system.retrieve(query, top_k=top_k)

        serializable_results = []
        for doc, score in results:
            serializable_results.append(
                {
                    "document": doc,
                    "score": float(score),
                }
            )

        return jsonify({"query": query, "results": serializable_results})
    except Exception as e:
        print(f"Error in search: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/document/<path:doc_id>", methods=["GET"])
def get_document(doc_id):
    try:
        document = None
        for doc in ir_system.documents:
            if doc.get("id") == doc_id:
                document = doc
                break

        if document is None:
            return jsonify({"error": "Document not found"}), 404

        return jsonify({"document": document})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/similar/<path:doc_id>", methods=["GET"])
def get_similar_documents(doc_id):
    try:
        top_k = request.args.get("top_k", default=5, type=int)

        doc_index = -1
        for idx, doc in enumerate(ir_system.documents):
            if doc.get("id") == doc_id:
                doc_index = idx
                break

        if doc_index == -1:
            return jsonify({"error": "Document not found"}), 404

        results = ir_system.retrieve_similar_documents(doc_index, top_k=top_k)

        serializable_results = []
        for doc, score in results:
            serializable_results.append(
                {
                    "document": doc,
                    "score": float(score),
                }
            )

        return jsonify({"document_id": doc_id, "results": serializable_results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/documents", methods=["GET"])
def get_documents():
    try:
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        documents = ir_system.documents[start_idx:end_idx]
        total = len(ir_system.documents)

        return jsonify(
            {
                "documents": documents,
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": (total + per_page - 1) // per_page,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    try:
        cache_stats = ir_system.get_cache_stats()

        stats = {
            "total_documents": len(ir_system.documents),
            "cache_stats": cache_stats,
        }

        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

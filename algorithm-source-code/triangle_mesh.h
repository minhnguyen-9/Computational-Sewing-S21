

#ifndef TRIANGLE_MESH_H
#define TRIANGLE_MESH_H

#include "include.h"
#include "triangle.h"
#include <map>

struct FaceDecl {
	unsigned int vertIdxs[3];
	unsigned int texIdxs[3];
};

struct TriangleMesh {
private:
	struct AdjacencyFaceTable { int adjIndices[3]; };
	std::vector<AdjacencyFaceTable> m_FaceAdjacencyTable;

	std::vector<Vector3> m_VertPos;
	std::vector<Vector3> m_VertTex;
	std::vector<FaceDecl> m_Faces;
	std::vector<Triangle> m_TexTris;
	std::vector<Triangle> m_PosTris;

	struct Panel {
		std::vector<unsigned> faceIdxs;
		std::vector<unsigned> vertTexIdxs;
		std::map<unsigned, unsigned> toPanelVertIdx;
	};
	std::vector<Panel> m_Panels;

	void ComputeAdjacency();
	void FloodFillTriangles(unsigned initialFace, std::vector<bool> & usedTris, std::vector<unsigned> & trisInRegion);
public:
	void Create(const char * fileName);

	size_t GetNumVerticesPos() {return m_VertPos.size(); }
	size_t GetNumVerticesTex() {return m_VertTex.size(); }
	size_t GetNumFaces() {return m_Faces.size(); }

	Triangle & GetTexTriangle(unsigned faceIdx) { return m_TexTris[faceIdx]; }
	Triangle GetTriangle3D(unsigned faceIdx) { return 
		Triangle(m_VertPos[m_Faces[faceIdx].vertIdxs[0]], m_VertPos[m_Faces[faceIdx].vertIdxs[1]], m_VertPos[m_Faces[faceIdx].vertIdxs[2]]); }

	void SetVertsPos(std::vector<Vector3> & verts) {
		if (verts.size() != m_VertPos.size()) __debugbreak();
		m_VertPos = verts;
	}
	std::vector<Vector3> & GetVertsPos() { return m_VertPos; }

	void Save(const std::string & fileName);
	void SavePanels(const char * dir, bool used3D=0);
	void LoadPanels(const char * dir);
	
	void Destroy() { m_FaceAdjacencyTable.clear(); m_VertPos.clear(); m_VertTex.clear(); m_Faces.clear(); m_Panels.clear(); m_PosTris.clear(); }
};

#endif
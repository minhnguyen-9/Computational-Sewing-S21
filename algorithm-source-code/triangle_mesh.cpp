
#include "triangle_mesh.h"
#include <fstream>

void GetFilesInDirectory(const char * dir, std::vector<std::string> & files) 
{
	WIN32_FIND_DATAA ffd;
	LARGE_INTEGER filesize;
	size_t length_of_arg;
	HANDLE hFind = INVALID_HANDLE_VALUE;
	DWORD dwError = 0;

	std::string str(dir); str += "\\*";
	hFind = FindFirstFileA(str.c_str(), &ffd);
	if (INVALID_HANDLE_VALUE == hFind) __debugbreak();

	files.clear();
	do {
		if (ffd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
		} else {
			files.push_back(dir);
			files.back() += "\\";
			files.back() += ffd.cFileName;
		}
	} while (FindNextFileA(hFind, &ffd) != 0);

	FindClose(hFind);
}

void TriangleMesh::FloodFillTriangles(unsigned initialFace, std::vector<bool> & usedTris, std::vector<unsigned> & trisInRegion)
{
	std::vector<unsigned> fhTris;
	fhTris.reserve(m_Faces.size());
	fhTris.push_back(initialFace);
	
	while (fhTris.size() != 0) {
		unsigned fhTri = fhTris.back(); fhTris.pop_back();

		if (usedTris[fhTri]) continue;
		usedTris[fhTri] = 1;

		trisInRegion.push_back(fhTri);
		for (unsigned i=0; i<3; i++) {
			auto adjIdx = m_FaceAdjacencyTable[fhTri].adjIndices[i];
			if (adjIdx != -1) {
				fhTris.push_back(adjIdx);
			}
		}
	}
}

void TriangleMesh::Create(const char * fileName)
{
	Destroy();

	auto AdvanceToWhiteSpace = [] (char * data, int & index) {
		while (data[index] != ' ' && data[index] != '\n' && data[index] != '\t' && data[index] != '\0') index++;
		if (data[index] == '\n') index--;
	};
	auto AdvanceToNonWhiteSpace = [] (char * data, int & index) {
		while ((data[index] == ' ' || data[index] == '\n' || data[index] == '\t') && data[index] != '\0') index++;
	};
	auto AdvanceToEndOfLine = [] (char * data, int & index) {
		while (data[index] != '\n' && data[index] != '\0') index++;
	};
	auto AdvanceToChar = [] (char * data, char ch, int & index) {
		while (data[index] != ch && data[index] != '\0') index++;
	};
	auto ReadFloat = [] (char * data, int & index, RScalar & flt) { // Does not work in all cases
		while (!isdigit(data[index]) && data[index] != '.' && data[index] != '+' && data[index] != '-' && data[index] != '\0') index++;
		flt = atof(data+index);
		while ((isdigit(data[index]) || data[index] == '.' || data[index] == 'e' || data[index] == '-' || data[index] == '+') && data[index] != '\0') index++;
	};
	auto ReadInt = [] (char * data, int & index, unsigned int & i) { // Does not work in all cases
		while (!isdigit(data[index]) && data[index] != '\0') index++;
		i = atoi(data+index);
		while (isdigit(data[index]) && data[index] != '\0') index++;
	};

	int len = 0;
	char * data = NULL;
	{
		std::ifstream stream(fileName);
		if (stream.fail()) {__debugbreak(); }
		stream.seekg(0, std::ios::end);
		len = (int)stream.tellg();
		data = new char[len+1];
		stream.seekg(0, std::ios::beg);
		stream.read(data, len);
	}
	data[len] = '\0';
	int index = 0;

	std::string text;
	while (data[index] != '\0') {
		char * text = data+index;
		if (text[0] == 'v' && text[1] != 'n' && text[1] != 't') {
			Vector3 pt;
			ReadFloat(data, index, pt[0]);
			ReadFloat(data, index, pt[1]);
			ReadFloat(data, index, pt[2]);
			m_VertPos.push_back(pt);
		}
		else if (text[0] == 'n' || (text[0] == 'v' && text[1] == 'n')) {
			Vector3 n;
			ReadFloat(data, index, n[0]);
			ReadFloat(data, index, n[1]);
			ReadFloat(data, index, n[2]);
		}
		else if (text[0] == 't' || (text[0] == 'v' && text[1] == 't')) {
			Vector3 t; t[2] = 0;
			ReadFloat(data, index, t[0]);
			ReadFloat(data, index, t[1]);
			m_VertTex.push_back(t);
		}
		else if (text[0] == 'v' && text[1] == 't') {
			AdvanceToEndOfLine(data, index);
		}
		else if (text[0] == 'f') {
			unsigned int vf1,vf2,vf3, tf1,tf2,tf3, nf1,nf2,nf3;

			// P, N
			ReadInt(data, index, vf1); if (data[index] == '/') {if (data[index+1] != '/') ReadInt(data, index, tf1); if (data[index] == '/') ReadInt(data, index, nf1); }
			ReadInt(data, index, vf2); if (data[index] == '/') {if (data[index+1] != '/') ReadInt(data, index, tf2); if (data[index] == '/') ReadInt(data, index, nf2); }
			ReadInt(data, index, vf3); if (data[index] == '/') {if (data[index+1] != '/') ReadInt(data, index, tf3); if (data[index] == '/') ReadInt(data, index, nf3); }
	
			m_Faces.push_back({{vf1-1, vf2-1, vf3-1}, {tf1-1, tf2-1, tf3-1}});
			m_TexTris.push_back({m_VertTex[tf1-1], m_VertTex[tf2-1], m_VertTex[tf3-1]});
			m_PosTris.push_back({m_VertPos[vf1-1], m_VertPos[vf2-1], m_VertPos[vf3-1]});
		}
		else {
			AdvanceToEndOfLine(data, index); index++;
		}
		AdvanceToNonWhiteSpace(data, index);
	};

	delete[] data;

	ComputeAdjacency();

	// Compute panels
	std::vector<bool> usedTris(m_Faces.size()); std::fill(usedTris.begin(), usedTris.end(), 0);
	while (1) {
		unsigned faceIdx = 0;
		for (; faceIdx<m_Faces.size(); faceIdx++) if (!usedTris[faceIdx]) break; 
		if (faceIdx >= m_Faces.size()) break;

		m_Panels.push_back({});
		auto & panelTris = m_Panels.back();
		FloodFillTriangles(faceIdx, usedTris, panelTris.faceIdxs);

		auto & tris = panelTris.faceIdxs;
		auto & newFaceVertIdxs = panelTris.toPanelVertIdx;
		for (unsigned j=0; j<tris.size(); j++) {
			for (unsigned k=0; k<3; k++) {
				auto vIdx = m_Faces[tris[j]].texIdxs[k];
				if (newFaceVertIdxs.find(vIdx) == newFaceVertIdxs.end()) {
					panelTris.vertTexIdxs.push_back(vIdx);
					newFaceVertIdxs[vIdx] = newFaceVertIdxs.size();
				}
			}
		}
	}
}

#include <map>
void TriangleMesh::ComputeAdjacency()
{
	using Edge = std::pair<unsigned, unsigned>;
	std::map<Edge, unsigned> edgeAdj;

	for (unsigned i=0; i<m_Faces.size(); i++) {
		auto & face = m_Faces[i];
		for (unsigned j=0; j<3; j++) {
			auto e = Edge(face.texIdxs[j], face.texIdxs[(j+1)%3]);
			if (edgeAdj.find(e) != edgeAdj.end()) __debugbreak();
			edgeAdj[e] = i;
		}
	}

	m_FaceAdjacencyTable.resize(m_Faces.size());
	for (unsigned i=0; i<m_Faces.size(); i++) {
		auto & face = m_Faces[i];
		for (unsigned j=0; j<3; j++) {
			auto eR = Edge(face.texIdxs[(j+1)%3], face.texIdxs[j]);
			if (edgeAdj.find(eR) != edgeAdj.end()) m_FaceAdjacencyTable[i].adjIndices[j] = edgeAdj[eR];
			else m_FaceAdjacencyTable[i].adjIndices[j] = -1;
		}
	}
}

void TriangleMesh::Save(const std::string & fileName)
{
	std::fstream stream(fileName, std::ios::out | std::ios::trunc);
	if (!stream) __debugbreak();

	for (unsigned i=0; i<m_VertPos.size(); i++) {
		Vector3 & v = m_VertPos[i];
		stream << "v " << v.x() << ' ' << v.y() << ' ' << v.z() << std::endl;
	}
	for (unsigned i=0; i<m_VertTex.size(); i++) {
		Vector3 & v = m_VertTex[i];
		stream << "vt " << v.x() << ' ' << v.y() << std::endl;
	}

	for (unsigned i=0; i<m_Faces.size(); i++) {
		stream << "f ";
		for (unsigned j=0; j<3; j++) {
			stream << m_Faces[i].vertIdxs[j]+1 << '/' << m_Faces[i].texIdxs[j]+1 << ' ';
		}
		stream << std::endl;
	}
}

void TriangleMesh::SavePanels(const char * dir, bool used3D)
{
	// Remove previous files in directory
	std::vector<std::string> files;
	GetFilesInDirectory(dir, files);
	for (unsigned i=0; i<files.size(); i++) {
		DeleteFileA(files[i].c_str());
	}

	char buf[256];
	for (unsigned i=0; i<m_Panels.size(); i++) {
		sprintf(buf, "%s\\panel_%.2i.obj", dir, i);
		std::fstream stream(buf, std::ios::out | std::ios::trunc);
		auto & panel = m_Panels[i];
		for (unsigned j=0; j<panel.vertTexIdxs.size(); j++) {
			const Vector3 & v = m_VertTex[panel.vertTexIdxs[j]];
			stream << "v " << v.x() << ' ' << v.y() << ' ' << 0 << std::endl;
		}
		if (used3D) {
			for (unsigned j=0; j<panel.faceIdxs.size(); j++) {
				Vector3 v = m_PosTris[panel.faceIdxs[j]].v[0];
				stream << "vt " << v.x() << ' ' << v.y() << ' ' << v.z() << std::endl;
				v = m_PosTris[panel.faceIdxs[j]].v[1];
				stream << "vt " << v.x() << ' ' << v.y() << ' ' << v.z() << std::endl;
				v = m_PosTris[panel.faceIdxs[j]].v[2];
				stream << "vt " << v.x() << ' ' << v.y() << ' ' << v.z() << std::endl;
			}
		} else {
			for (unsigned j=0; j<panel.faceIdxs.size(); j++) {
				Vector3 v = m_TexTris[panel.faceIdxs[j]].v[0];
				stream << "vt " << v.x() << ' ' << v.y() << ' ' << v.z() << std::endl;
				v = m_TexTris[panel.faceIdxs[j]].v[1];
				stream << "vt " << v.x() << ' ' << v.y() << ' ' << v.z() << std::endl;
				v = m_TexTris[panel.faceIdxs[j]].v[2];
				stream << "vt " << v.x() << ' ' << v.y() << ' ' << v.z() << std::endl;
			}
		}
		for (unsigned j=0; j<panel.faceIdxs.size(); j++) {
			stream << "f ";
			for (unsigned k=0; k<3; k++) {
				auto vIdx = panel.toPanelVertIdx[m_Faces[panel.faceIdxs[j]].texIdxs[k]];
				stream << vIdx+1 << '/' << j*3+k+1 << ' ';
			}
			stream << std::endl;
		}
	}
}

#include <iostream>

void TriangleMesh::LoadPanels(const char * dir)
{
	std::vector<std::string> files;
	GetFilesInDirectory(dir, files);
	if (files.size() == 0) __debugbreak();

	unsigned count=0;
	for (unsigned i=0; i<files.size() && count < m_Panels.size(); i++) {
		if (files[i].find(".txt") != std::string::npos) {
			std::cout << files[i] << std::endl;
			auto & panel = m_Panels[count];
			std::fstream stream(files[i], std::ios::in);
			for (unsigned j=0; j<panel.vertTexIdxs.size(); j++) {
				Vector3 & v = m_VertTex[panel.vertTexIdxs[j]];
				stream >> v.x();
				stream >> v.y();
			}
			count++;
		}
	}

	// Fix m_TexTris
	RScalar a=0,b=0;
	for (unsigned i=0; i<m_Faces.size(); i++) {
		const auto & v1 = m_VertTex[m_Faces[i].texIdxs[0]];
		const auto & v2 = m_VertTex[m_Faces[i].texIdxs[1]];
		const auto & v3 = m_VertTex[m_Faces[i].texIdxs[2]];
		//a+= m_TexTris[i].Area();
		m_TexTris[i] = Triangle(v1, v2, v3);
		//b+= m_TexTris[i].Area();
	}
	//std::cout << a << ' ' << b << std::endl;
}















	/*
	// Func signature: unsigned faceIndex, VertexDecl & v1, VertexDecl & v2, VertexDecl & v3
	template <typename Func>
	void IterateFacesVertexPos(Func func) {
		for (unsigned int i=0, end=(unsigned)m_Faces.size(); i<end; i++) {
			FaceDecl & face = m_Faces[i];
			func(i, m_VertPos[face.vertIdxs[0]], m_VertPos[face.vertIdxs[1]], m_VertPos[face.vertIdxs[2]]); 
		}
	};
	template <typename Func>
	void IterateFacesVertexTex(Func func) {
		for (unsigned int i=0, end=(unsigned)m_Faces.size(); i<end; i++) {
			FaceDecl & face = m_Faces[i];
			func(i, m_VertTex[face.texIdxs[0]], m_VertTex[face.texIdxs[1]], m_VertTex[face.texIdxs[2]]); 
		}
	};

	// Indices
	template <typename Func>
	void IterateFaceVertexPosIndices(Func func) {
		for (unsigned int i=0, end=(unsigned)m_Faces.size(); i<end; i++) {
			FaceDecl & face = m_Faces[i];
			func(face.vertIdxs[0], face.vertIdxs[1], face.vertIdxs[2], i); 
		}
	};
	template <typename Func>
	void IterateFaceVertexTexIndices(Func func) {
		for (unsigned int i=0, end=(unsigned)m_Faces.size(); i<end; i++) {
			FaceDecl & face = m_Faces[i];
			func(face.texIdxs[0], face.texIdxs[1], face.texIdxs[2], i); 
		}
	};
	template <typename Func>
	bool IterateVertexFaceIndices(int vertIdx, Func func) {
		int faceIndex = m_VertToFaceIndex[vertIdx];
		int initialFaceIndex = m_VertToFaceIndex[vertIdx];
		int preFaceIndex = faceIndex;
		do {
			preFaceIndex = faceIndex;

			int vIdx = 0;
			for (int i=0; i<3; i++) {if (faces[faceIndex].indices[i] == vertIdx) break; vIdx++; }
			if (faces[faceIndex].indices[vIdx] != vertIdx) {
				//if (faces[faceIndex].indices[vIdx] != Vector3) {
				//faces[faceIndex].c = Vector3(0, 1, 0);
				return 0;
			}

			func(faces[faceIndex].indices[vIdx], faces[faceIndex].indices[(vIdx+1)%3], faces[faceIndex].indices[(vIdx+2)%3], faceIndex);
			faceIndex = m_FaceAdjacencyTable[faceIndex].adjIndices[mod(vIdx-1, 3)];
		} while (faceIndex != -1 && faceIndex != initialFaceIndex);// && preFaceIndex != faceIndex);

		return faceIndex != -1;
	};*/
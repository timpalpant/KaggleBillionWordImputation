#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <exception>
 
using namespace std;
 
int getnext_utf8_byte(istream &fd);
void write_utf8byte(ostream &fd, const int &u);
void write_utf8byte_quoted(ostream &fout, const int &u);
char get_next_byte(istream& fd);
ostream& operator << (ostream& os, vector<int> &str);
 
class XmlNode
{
public:
     string tagname;
     vector<int> data;//stores uft8 string as vector<int>
     map< string, string > attributes;
 
     void readtagname(istream &fd, int &a);
     void readattributes(istream &fd, int &a);
     void readtagclose(istream &fd, int &a);
     void readnodevalue(istream &fd, int &a);
};
 
//-----------------------------------------------------------------------------
int main(int argc, char* argv[])
{
    bool inpage=false;
 
    //for debugging
    cout.unsetf(ios::dec);
    cout.setf(ios::hex);
 
    istream& fd = cin;
    ostream& fout = cout;
 
    try{
 
        int a = getnext_utf8_byte(fd);
        bool had_text = false;
        bool inrevision = false;
        while (fd.good())
        {
            if (a==0x3C)//'<'
            {
                XmlNode node;
                node.readtagname(fd, a);
                node.readattributes(fd, a);
                node.readtagclose(fd, a);
                node.readnodevalue(fd, a);
 
                if(node.tagname=="page")
                {
                    inpage=true;
                    had_text=false;
                }
                else if(node.tagname=="/page")
                {
                    inpage=false;
                    if (!had_text) {
                      fout << "null);";
                    }
                }
                else if(inpage && node.tagname=="revision") {
                    inrevision = true;
                }
                else if(inpage && node.tagname=="/revision") {
                    inrevision = false;
                }
                else if(inpage && !inrevision && node.tagname=="id")
                {
                    fout << "insert ignore into `page_text`(`page_id`,`page_text`) values('";
                    for(int i=0, x=node.data.size(); i<x; i++)
                        write_utf8byte_quoted(fout, node.data[i] );
                    fout << "',";
                }
                else if(inpage && node.tagname=="text")
                {
                    had_text = true;
                    fout << "'";
                    for(int i=0, x=node.data.size(); i<x; i++)
                        write_utf8byte_quoted(fout, node.data[i] );
                    fout << "');"<<endl;                
                }
 
            }//if (a==0x3C)//'<'
 
        }//while (fd.good())
    }
    catch(exception &e)//end of file exception will be thrown
    {
        cout << e.what() <<endl;
    }
 
    return 0;
}
//-----------------------------------------------------------------------------
void XmlNode::readtagname(istream &fd, int &a)
{
    string tagname;
    a = getnext_utf8_byte(fd);
    while (a!=0x20 && a!=0x3E)//' '
    {
        tagname+= ( (0<=a && a<=127) ? (char)a : '?' );
        a = getnext_utf8_byte(fd);
    }
    this->tagname=tagname;
}
//-----------------------------------------------------------------------------
void XmlNode::readattributes(istream &fd, int &a)
{
    string token;
    string attribute_name;
    while (1)//start xml attributes
    {
        while (a==0x20) { a = getnext_utf8_byte(fd); }//eat whitespace
 
        while (a!=0x20 && a!=0x3D && a!=0x3E)//' ','=','>'
        {
            token+= ( (0<=a && a<=127) ? (char)a : '?' );
            a = getnext_utf8_byte(fd);
        }
 
        while (a==0x20) { a = getnext_utf8_byte(fd); }//eat whitespace
 
        if (a==0x3D)//'='
        {
            a = getnext_utf8_byte(fd);
 
            attribute_name=token; token.clear();
            while (a==0x20) { a = getnext_utf8_byte(fd); }//eat whitespace
 
            char delimiter = (char)a;
            if (delimiter==0x22 || delimiter==0x29)//'"','\''
            {
                a = getnext_utf8_byte(fd);
 
                while (a!=delimiter && a!=0x3E)//' ','=','>'
                {
                    token+= ( (0<=a && a<=127) ? (char)a : '?' );
                    a = getnext_utf8_byte(fd);
                }
                this->attributes[ attribute_name ] = token; token.clear();
            }
        }
        while (a==0x20) { a = getnext_utf8_byte(fd); }//eat whitespace
        if    (a==0x2f) { a = getnext_utf8_byte(fd); }//eat /
        if    (a==0x3E) { break;                     }//break on >
 
         a = getnext_utf8_byte(fd);
    }//while (1) //end xml attributes
}
//-----------------------------------------------------------------------------
void XmlNode::readtagclose(istream &fd, int &a)
{
    if    (a==0x3E)  { a = getnext_utf8_byte(fd);  }//eat >
}
//-----------------------------------------------------------------------------
void XmlNode::readnodevalue(istream &fd, int &a)
{
    while (a!=0x3C)//'<'  read nodevalue
    {
        if (a==0x26)//if &
        {
            string token;
            while (a!=0x3b)// eat until ;
            {
                token+= ( (0<=a && a<=127) ? (char)a : '?' );
                a = getnext_utf8_byte(fd);
            }
            token+= ( (0<=a && a<=127) ? (char)a : '?' );
            a = getnext_utf8_byte(fd);
            if (token=="\"") this->data.push_back((int)'"');
            if (token=="<")   this->data.push_back((int)'<');
            if (token=="&gt;")   this->data.push_back((int)'"&gt;');
            if (token=="&")  this->data.push_back((int)'&');
        }
        else//regular utf8 char (not ampersand entity)
        {
            this->data.push_back(a);
            a = getnext_utf8_byte(fd);
        }
    }
}
//-----------------------------------------------------------------------------
int getnext_utf8_byte(istream &fd)
{
    char arr[4];
 
    arr[0]=get_next_byte(fd);
    if ((arr[0]&0x80)==0)
        return arr[0]&0x7F;
 
    arr[1]=get_next_byte(fd);
    if ((arr[0]&0x20)==0 && (arr[1]&0x40)==0)
        return ((arr[0]&0x1F) << 6) | (arr[1]&0x3F);
 
    arr[2]=get_next_byte(fd);
    if ((arr[0]&0x10)==0 && (arr[1]&0x40)==0 && (arr[2]&0x40)==0)
        return ((arr[0]&0x0F) << 12) | ((arr[1]&0x3F) << 6) | (arr[2]&0x3F);
 
    arr[3]=get_next_byte(fd);
    if ((arr[0]&0x08)==0 && (arr[1]&0x40)==0 && (arr[2]&0x40)==0 && (arr[3]&0x40)==0)
    return ((arr[0]&0x07) << 18) | ((arr[1]&0x3F) << 12) | ((arr[2]&0x3F) << 6) | (arr[3]&0x3F);
 
    cerr << "Invalid UTF8 Character "<<endl;
    fd.putback(arr[3]);
    fd.putback(arr[2]);
    fd.putback(arr[1]);
    return 0x00;
}
//-----------------------------------------------------------------------------
char get_next_byte(istream& fd)
{
    char a;
    fd.get(a);
    if (!fd.good()) throw ios_base::failure("end of file");
    return a;
}
//-----------------------------------------------------------------------------
ostream& operator << (ostream& os, vector<int> &str)
{//for debugging
    for(int i=0; i<str.size(); i++)
    {
        if (32<= str[i] && str[i]<=127)
            os << (  (char)str[i]  );
        else
            os << "?";
    }
    return os;
}
//-----------------------------------------------------------------------------
void write_utf8byte_quoted(ostream &fout, const int &u)
{
    if      (u==0x00) fout <<"\\x00";
    else if (u==0x0a) fout <<"\\n";
    else if (u==0x0d) fout <<"\\r";
    else if (u==0x5c) fout <<"\\\\";//"
    else if (u==0x27) fout <<"\\'";
    else if (u==0x22) fout <<"\\\"";
    else if (u==0x1a) fout <<"\\x1a";
    else        
        write_utf8byte(fout, u );
}
//-----------------------------------------------------------------------------
void write_utf8byte(ostream &fd, const int &u)
{
    char bytes[4];
 
    int bytecount=1;
    if (u>= 65536)//4 : 2^16
    {                              
        bytes[0]= 0x000000F0 | ((0x001C0000 & u) >> 18);
        bytes[1]= 0x00000080 | ((0x0003F000 & u) >> 12);
        bytes[2]= 0x00000080 | ((0x00000FC0 & u) >> 6);
        bytes[3]= 0x00000080 | ((0x0000003F & u) >> 0);
        bytecount=4;
    }
    else if (u>=2048)//3 : 2^11
    {
        bytes[0]= 0x000000E0 | ((0x0000F000 & u) >> 12);
        bytes[1]= 0x00000080 | ((0x00000FC0 & u) >> 6);
        bytes[2]= 0x00000080 | ((0x0000003F & u) >> 0);
        bytecount=3;
    }
    else if (u>=128)//2 : 2^7
    {
        bytes[0]= 0x000000C0 | ((0x000007C0 & u) >> 6);
        bytes[1]= 0x00000080 | ((0x0000003F & u) >> 0);
        bytecount=2;
    }
    else //1
    {
        bytes[0]= 0x0000007F & u;
        bytecount=1;
    }
    fd.write(bytes,bytecount);
}
//-----------------------------------------------------------------------------